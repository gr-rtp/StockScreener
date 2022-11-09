# import general purpose modules
import datetime
import pandas as pd
from tqdm import tqdm

# import modules for data fetching
import yfinance as yf

# import modules for database reading and writing to database
from technical.stock_price_service import Stock_Price
from technical.index_price_service import Index_Price

# import helper functions and variables
from technical.helpers import get_table_name, index_data, available_indexes, major_indexes, get_last_busyday

# import technical analysis functions
from technical.technical_analysis import calc_sma_volume, get_high_low, get_relative_strength, get_weighted_comp, get_dates

INITIAL_DATE = datetime.date.fromisoformat("2019-04-14")
SHORT_START = get_last_busyday((datetime.date.today() - datetime.timedelta(days=7)).isoformat())



class Data_Pipeline():
    def __init__(self):
        self.stock_price_service = Stock_Price()
        self.index_price_service = Index_Price()

        self.update_from = INITIAL_DATE
        self._260_DAYS = datetime.timedelta(260)
        self.today = datetime.date.today()
        self.yesterday: datetime.date = get_last_busyday()
        return



    def load_stock_prices(self, symbol: str, index, start_date=INITIAL_DATE):
        """
        Fetches price data for the specified symbol from the provided start date to the most recently finished day
        """
        start_date_ts = pd.Timestamp(start_date)

        table_name = get_table_name(index, symbol)

        yesterday = datetime.date.today()

        # get price data since start_date till past day's date
        if symbol[0] == "^":
            symbol_data = yf.Ticker(symbol)
        else:
            symbol_data = yf.Ticker(symbol + index_data[index]['suffix'])

        prices = symbol_data.history(start=start_date.isoformat(), end=yesterday.isoformat(), actions=False)

        if prices.empty:
            return

        prices.reset_index(inplace=True)
        new_prices = prices.to_numpy()

        price_list = []

        for day_price in new_prices:
            if start_date_ts > day_price[0]:
                continue

            price_tuple = (day_price[0], day_price[1], day_price[4], day_price[2], day_price[3], day_price[5])
            price_list.append(price_tuple)

        self.stock_price_service.init_table(table_name, symbol)
        
        self.stock_price_service.bulk_add_stock(table_name, (*price_list,))
        return


    def update_stocks_of_index(self, index):
        print("===== Updating Price, SMA, Volume & Relative Strength for the " + index + " Index =====")

        index_table_name = get_table_name(index, index_data[index]['symbol'])

        index_last_date = None
        index_yesterday = self.yesterday

        index_table_exists = self.stock_price_service.table_exists(index_table_name)
        df_index_weighted_comp = None

        if index_table_exists:
                index_last_date = self.stock_price_service.get_last_price(index_table_name)

                if index_last_date is not None:
                    index_last_date = index_last_date[1]

                    if index_last_date == index_yesterday:
                        index_period = (self.today - (INITIAL_DATE - self._260_DAYS)).days

                        df_index_weighted_comp = get_weighted_comp(self.stock_price_service.get_some_prices(index_table_name, index_period, 0, ['date', 'close'], "DESC")[::-1], INITIAL_DATE)
                    else:
                        index_start = index_last_date + datetime.timedelta(days=1)
                        print("Updating " + index_table_name + " from: " + index_start.isoformat() + " to: " + index_yesterday.isoformat())

                        # get index values or load index if not available
                        self.load_stock_prices(index_data[index]['symbol'], index, index_start)
                        self.load_stock_sma_volume(index_table_name, index_start)
                        self.load_stock_highs_lows(index_table_name, index_start)

                        index_period = (self.today - (SHORT_START - self._260_DAYS)).days

                        # calculate cum_prod
                        df_index_weighted_comp = get_weighted_comp(self.stock_price_service.get_some_prices(index_table_name, index_period, 0, ['date', 'close'], "DESC")[::-1], SHORT_START)
                        
        else:
            # get index values or load index if not available
            self.load_stock_prices(index_data[index]['symbol'], index)

            if self.stock_price_service.table_exists(index_table_name):
                self.load_stock_sma_volume(index_table_name)
                self.load_stock_highs_lows(index_table_name)

                index_period = (self.today - (SHORT_START - self._260_DAYS)).days

                df_index_weighted_comp = get_weighted_comp(self.stock_price_service.get_some_prices(index_table_name, index_period, 0, ['date', 'close'], "DESC")[::-1], SHORT_START)


        for stock in tqdm(index_data[index]['components']):
            symbol: str = stock
            if symbol.endswith(index_data[index]['suffix']):
                symbol = symbol.removesuffix(index_data[index]['suffix'])
            
            table_name = get_table_name(index, symbol)

            table_exists = self.stock_price_service.table_exists(table_name)

            last_date = None
            yesterday = self.yesterday

            if table_exists:
                last_date = self.stock_price_service.get_last_price(table_name)

                if last_date is not None:
                    last_date = last_date[1]

                    if last_date == yesterday:
                        continue
                    else:
                        start = last_date + datetime.timedelta(days=1)
                        # print("Updating " + table_name + " from: " + start.isoformat() + " to: " + yesterday.isoformat())

                        self.load_stock_prices(symbol, index, start)
                        self.load_stock_sma_volume(table_name, start)
                        self.load_stock_highs_lows(table_name, start)

                        stock_period = (self.today - (SHORT_START - self._260_DAYS)).days

                        df_stock_weighted_comp = get_weighted_comp(self.stock_price_service.get_some_prices(table_name, stock_period, 0, ['date', 'close'], "DESC")[::-1], SHORT_START)
                        self.load_stock_relative_strength(table_name, df_index_weighted_comp, df_stock_weighted_comp)
            else:
                # print("---------------->  Adding New Table: " + table_name)
                self.load_stock_prices(symbol, index)

                if not self.stock_price_service.table_exists(table_name):
                    continue

                self.load_stock_sma_volume(table_name)
                self.load_stock_highs_lows(table_name)

                stock_period = (self.today - (SHORT_START - self._260_DAYS)).days

                if df_index_weighted_comp is None:
                    continue

                df_stock_weighted_comp = get_weighted_comp(self.stock_price_service.get_some_prices(table_name, stock_period, 0, ['date', 'close'], "DESC")[::-1], SHORT_START)

                self.load_stock_relative_strength(table_name, df_index_weighted_comp, df_stock_weighted_comp)
        
        # print("+++++++++++ " + index + " Finished +++++++++++")
        return

    def update_all_stocks(self):
        """
        Updates each index and stock price from the last date in each table till the last recently ended date
        after loading prices, calculates moving avarages of price and volumes
        then finds the highs and lows of the same period
        and finally calculates the relative strength using the weighted cummulative product of the index and each stock
        """

        # load prices since last day till previous day
        for index in available_indexes:
            self.update_stocks_of_index(index)
        return



    def update_all_relative_strength_sp500(self, start_date = SHORT_START, end_date = None):
        """
        Calculates and uploads the relative strength for each stock based on a target index, in this case the S&P500
        """

        if end_date is None:
            end_date = self.today

        for reference_index in major_indexes:
            
            for index in available_indexes:
                print("===== Updating Relative Strength for the " + index + " Index against S&P500 =====")

                self.update_reference_relative_strength(reference_index, index, 'relative_strength_sp500', start_date, end_date)
        return



    def update_own_relative_strength(self, index, start_date = SHORT_START, end_date = None):
        """
        Calculates and uploads the relative strength for each stock based on it's own index
        """

        if end_date is None:
            end_date = self.today

        index_table_name = get_table_name(index, index_data[index]['symbol'])

        df_reference_index_weighted_comp = get_weighted_comp(self.stock_price_service.get_prices_between_dates(index_table_name, get_dates(start_date, 260)[3].astype(datetime.date), end_date), start_date)

        print("===== Updating own Relative Strength for the " + index + " Index =====")

        for stock in tqdm(index_data[index]['components']):
            symbol: str = stock
            if symbol.endswith(index_data[index]['suffix']):
                symbol = symbol.removesuffix(index_data[index]['suffix'])
            
            table_name = get_table_name(index, symbol)

            table_exists = self.stock_price_service.table_exists(table_name)

            if table_exists:

                last_row = self.stock_price_service.get_last_price(table_name)[-1]

                if end_date == self.today and last_row is not None:
                    print('relative_strength is up to date for ' + stock)
                    continue

                # stock_period = (self.today - (start_date - self._260_DAYS)).days

                # calculate cum_prod
                df_stock_weighted_comp = get_weighted_comp(self.stock_price_service.get_prices_between_dates(table_name, get_dates(start_date, 260)[3].astype(datetime.date), end_date), start_date)

                if df_stock_weighted_comp is None or df_stock_weighted_comp.empty:
                    continue

                self.load_stock_relative_strength(table_name, df_reference_index_weighted_comp, df_stock_weighted_comp)
        return


    
    def update_reference_relative_strength(self, ref_index: str, stocks_index, destination_column, start_date = SHORT_START, end_date = None):
        """
        Calculates and uploads the relative strength for each stock based on a target index, in this case the S&P500
        """

        if end_date is None:
            end_date = self.today

        index_table_name = get_table_name(ref_index, index_data[ref_index]['symbol'])

        df_reference_index_weighted_comp = get_weighted_comp(self.stock_price_service.get_prices_between_dates(index_table_name, get_dates(start_date, 260)[3].astype(datetime.date), end_date), start_date)

        print("===== Updating " + ref_index + " Relative Strength for the " + stocks_index + " Index =====")

        for stock in tqdm(index_data[stocks_index]['components']):
            symbol: str = stock
            if symbol.endswith(index_data[stocks_index]['suffix']):
                symbol = symbol.removesuffix(index_data[stocks_index]['suffix'])
            
            table_name = get_table_name(stocks_index, symbol)

            table_exists = self.stock_price_service.table_exists(table_name)

            if table_exists:
                last_row = self.stock_price_service.get_last_price(table_name)[-1]

                if end_date == self.today and last_row is not None:
                    # print("relative_strength_" + ref_index.lower() + " is up to date for " + stock)
                    continue

                # stock_period = (self.today - (start_date - self._260_DAYS)).days

                # calculate cum_prod
                df_stock_weighted_comp = get_weighted_comp(self.stock_price_service.get_prices_between_dates(table_name, get_dates(start_date, 260)[3].astype(datetime.date), end_date), start_date)

                if df_stock_weighted_comp is None or df_stock_weighted_comp.empty:
                    continue


                self.load_stock_relative_strength(table_name, df_reference_index_weighted_comp, df_stock_weighted_comp, destination_column)
        return



    def load_stock_sma_volume(self, symbol, start=None):
        """
        Loads SMAs and Volume Averages into database tables
        """
        period = "max"
        days = None

        if start is not None:
            delta = (datetime.date.today() - datetime.timedelta(days=1)) - start
            days = delta.days + 1
            period = 200 + days

        # get symbol price data from database from latest date to earlier
        historical_prices = self.stock_price_service.get_some_prices(symbol, period, 0, ['date','close','volume'], 'DESC')

        if len(historical_prices) == 0:
            return

        # calculate technicals
        # reverse historical prices to be in ascending order for rolling average
        technicals = calc_sma_volume(historical_prices[::-1])

        if len(technicals) == 0:
            return

        # store results in database
        if start is None:
            self.stock_price_service.bulk_add_sma_volume(symbol, technicals)
        else:
            snip = days * -1
            self.stock_price_service.bulk_add_sma_volume(symbol, technicals[snip:])
        return



    def load_stock_highs_lows(self, symbol, start=None):
        """
        Loads 52 week highs and lows
        """
        days = None
        period = "max"

        if start is not None:
            delta = (datetime.date.today() - datetime.timedelta(days=1)) - start
            days = delta.days + 1
            period = 240 + days

        # get symbol price data from database
        historical_prices = self.stock_price_service.get_some_prices(symbol, period, 0, ['date','high','low'], 'DESC')

        if len(historical_prices) == 0:
            return

        # calculate technicals
        highs_lows = get_high_low(historical_prices[::-1])

        if len(highs_lows) == 0:
            return

        # store results in database
        if start is None:
            self.stock_price_service.bulk_update_stock(symbol, ['date', 'high_52_week', 'low_52_week'], highs_lows)
        else:
            snip = days * -1
            self.stock_price_service.bulk_update_stock(symbol, ['date', 'high_52_week', 'low_52_week'], highs_lows[snip:])
        return



    def load_stock_relative_strength(self, symbol, index_cum_prod, stock_cum_prod, column = 'relative_strength'):
        tuple_list = get_relative_strength(index_cum_prod, stock_cum_prod)

        if len(tuple_list) > 0:
            self.stock_price_service.bulk_update_stock(symbol, ['date', column], tuple_list)



    def load_stock_relative_strength_sp500(self, symbol, index_cum_prod, stock_cum_prod):
        self.load_stock_relative_strength(symbol, index_cum_prod, stock_cum_prod, 'relative_strength_sp500')

        

    def get_first_date(self):

        # reference stock (last stock that will be updated if full update is completed)
        table_name = get_table_name('NASDAQ', 'ZYXI')
        
        first_date = self.stock_price_service.get_first_price(table_name)[1]

        return first_date



    def get_last_update(self):

        # reference stock (last stock that will be updated if full update is completed)
        
        table_name = get_table_name('NASDAQ', 'ZYXI')
        
        last_date = self.stock_price_service.get_last_price(table_name)[1]

        return last_date


    def get_total_dates(self):

        # reference stocks (last stock that will be updated if full update is completed)
        reference_stocks = ['zyxi_nasdaq', 'zyme_nyse', 'zts_s_p500', 'wmt_dow']

        for stock in reference_stocks:
            table_exists = self.stock_price_service.table_exists(stock)
            if table_exists:
                last_price = self.stock_price_service.get_last_price(stock)
                first_date = self.stock_price_service.get_first_price(stock)[1]
                last_date = last_price[1]
                total_dates = last_price[0]

                sum = "Total avaliable data is " + str(total_dates) + " trading days from " + first_date.isoformat() + " to " + last_date.isoformat()
                break
        
        return sum

    def get_total_stocks(self):
        
        total_stocks = self.stock_price_service.get_total_stocks()

        sum = "\nTotal number of stocks in database: \n" + "DOW: " + str(total_stocks[1]) + "\n" + "S&P500: " + str(total_stocks[2]) + "\n" + "NYSE: " + str(total_stocks[3]) + "\n" + "NASDAQ: " + str(total_stocks[4]) + "\n\n" + "All indexes: "+ str(total_stocks[0])

        return sum


data_pipeline = Data_Pipeline()