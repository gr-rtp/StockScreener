from technical.stock_price_service import Stock_Price
from technical.technical_analysis import calc_sma_volume, get_high_low, get_dates, get_weighted_comp, get_relative_strength
from technical.helpers import get_table_name
import pandas as pd
import pandas.testing as pd_testing
import numpy as np
import datetime

import requests
import fundamental.alphav as alphav

INITIAL_DATE = datetime.date.fromisoformat("2019-04-15")

stock_price = Stock_Price()

class Unit_Test():
    
    """To test the functionality and accuracy of each key function, results in dataframe generated by the application is compared with resulted calculated in Excel.
        The overall testing results show that all of the key functions including get_sma_volume, get_high_low, get_weighted_comp and get_relative_strength return
        same results as suggested by Excel indicating the functions work correctly and provide accurate results. 
    """

    def __init__(self):
        pass

    def test_get_sma_volume(self, index, ticker, start, end_date):
        table_name = get_table_name(index,ticker)

        historical_prices = stock_price.get_prices_between_dates(table_name, start, end_date, ['date','close','volume'])

        sma_volume = calc_sma_volume(historical_prices)

        #sma and volume calculated by the application
        df_sma_volume = pd.DataFrame(sma_volume, columns= ['date','sma10','sma50','sma100','sma150','sma200','volume10','volume50','volume100','volume150','volume200'])
        df_sma_volume['date'] = pd.to_datetime(df_sma_volume['date'])

        #sma and volume calculated by Excel
        df_sma_volume_excel = pd.read_csv(r'testing\get_sma_volume_aapl_2022-05-20.csv', dayfirst=True, parse_dates=[0])

        test_case_sma_volume = pd_testing.assert_frame_equal(df_sma_volume, df_sma_volume_excel)

        if test_case_sma_volume is None:
            print('Test Case_SMA & Volume: Passed')

    def test_get_high_low(self, index, ticker, start, end_date):
        table_name = get_table_name(index,ticker)

        historical_prices = stock_price.get_prices_between_dates(table_name, start, end_date, ['date','high','low'])

        high_low = get_high_low(historical_prices)

        #high calculated by the application
        df_hign_low = pd.DataFrame(high_low, columns= ['date','high_52_week','low_52_week'])
        df_hign_low['date'] = pd.to_datetime(df_hign_low['date'])

        # high and low calculated by Excel
        df_hign_low_excel = pd.read_csv(r'testing\get_hign_low_aapl_2022-05-20.csv', dayfirst=True, parse_dates=[0])

        test_case_hign_low = pd_testing.assert_frame_equal(df_hign_low, df_hign_low_excel)

        if test_case_hign_low is None:
            print('Test Case_52-Week High_Low: Passed')

    def test_get_weighted_comp(self, index, ticker, start, end_date, min_days):

        table_name = get_table_name(index,ticker)

        if min_days < 9:
            from_date = INITIAL_DATE
        else:
            from_date = get_dates(start, min_days)[3].astype(datetime.date)

        historical_prices = stock_price.get_prices_between_dates(table_name, from_date, end_date, ['date','close'])
        weighted_comp = get_weighted_comp(historical_prices, start)

        #weighted_comp calculated by the application
        df_weighted_comp = pd.DataFrame(weighted_comp, columns= ['date','Weighted_comp'])
        df_weighted_comp['date'] = pd.to_datetime(df_weighted_comp['date'])
        df_weighted_comp.reset_index(inplace = True, drop = True)
 
        #weighted_comp calculated by Excel
        df_weighted_comp_excel = pd.read_csv(r'testing\get_weighted_comp_aapl_2022-05-27.csv', dayfirst=True, parse_dates=[0])

        test_case_weighted_comp = pd_testing.assert_frame_equal(df_weighted_comp, df_weighted_comp_excel)

        if test_case_weighted_comp is None:
            print('Test Case_Weighted_comp: Passed')

    def test_get_relative_strength(self, stock_index, stock_symbol, reference_index, reference_index_symbol, start, end_date, min_days):

        stock_table_name = get_table_name(stock_index,stock_symbol)
        index_table_name = get_table_name(reference_index, reference_index_symbol)

        if min_days < 9:
            from_date = INITIAL_DATE
        else:
            from_date = get_dates(start, min_days)[3].astype(datetime.date)

        stock_historical_prices = stock_price.get_prices_between_dates(stock_table_name, from_date, end_date, ['date','close'])
        stock_weighted_comp = get_weighted_comp(stock_historical_prices, start)
        df_stock_weighted_comp = pd.DataFrame(stock_weighted_comp, columns= ['date','Weighted_comp'])
        df_stock_weighted_comp['date'] = pd.to_datetime(df_stock_weighted_comp['date'])

        index_historical_prices = stock_price.get_prices_between_dates(index_table_name, from_date, end_date, ['date','close'])
        index_weighted_comp = get_weighted_comp(index_historical_prices, start)
        df_index_weighted_comp = pd.DataFrame(index_weighted_comp, columns= ['date','Weighted_comp'])
        df_index_weighted_comp['date'] = pd.to_datetime(df_index_weighted_comp['date'])

        # relative strength calculated by the application
        relative_strength = get_relative_strength(df_index_weighted_comp, df_stock_weighted_comp)
        df_relative_strength = pd.DataFrame(relative_strength, columns=['date', 'relative_strength'])

        df_stock_weighted_comp.reset_index(inplace = True, drop = True)

        #relative strength calculated by Excel
        df_relative_strength_excel = pd.read_csv(r'testing\get_relative_strength_aapl_2022-05-27.csv', dayfirst=True, parse_dates=[0])

        test_case_relative_strength = pd_testing.assert_frame_equal(df_relative_strength, df_relative_strength_excel)

        if test_case_relative_strength is None:
            print('Test Case_Relative_Strength: Passed')

    # unitest of fundamental fucntion to get eps
    def get_eps_info_test(self, symbol):
        api_url = "https://www.alphavantage.co/query"
        params = {
            "function": "EARNINGS",
            "symbol": symbol,
            "apikey": "A3SOTUU1TNEPHRR2",
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        List, price_change_list = alphav.get_eps_info(symbol)

        if (len(data['quarterlyEarnings']) > 17):
            return len(List) == 16
        else:
            return len(List) == len(data['quarterlyEarnings'])-2;

    def execute_unittests(self):
        stock_index = 'DOW'
        stock_symbol = 'AAPL'
        # stock_table_name = get_table_name(stock_index,stock_symbol)

        index = 'S&P500'
        index_symbol = '^GSPC'

        # test date set #1
        start_set1 = datetime.date.fromisoformat("2019-04-15")
        end_date_set1 = datetime.date.fromisoformat("2022-05-20")

        # test date set #2
        start_set2 = datetime.date.fromisoformat("2021-05-27")
        end_date_set2 = datetime.date.fromisoformat("2022-05-27")
        avaialble_data = 300

        # test cases SMA & Volume
        print('============ Unit Testing Results ============')
        print('\nTest date: 2022-05-22')
        print('Stock: ' + stock_symbol)
        print('Start date: ' + str(start_set1) + '   End date: ' + str(end_date_set1) + '\n')
        self.test_get_sma_volume(stock_index,stock_symbol,start_set1, end_date_set1)
        self.test_get_high_low(stock_index,stock_symbol,start_set1, end_date_set1)

        print('\n---------------------------------------------')
        print('\nTest date: 2022-05-27')
        print('Stock: ' + stock_symbol + ' Index: S&P500')
        print('Start date: ' + str(start_set2) + '   End date: ' + str(end_date_set2) + '\n')
        self.test_get_weighted_comp(stock_index, stock_symbol, start_set2, end_date_set2, avaialble_data)
        self.test_get_relative_strength(stock_index, stock_symbol, index, index_symbol, start_set2, end_date_set2, avaialble_data)

        print('\n---------------------------------------------')
        print("\nget_eps_info_test")
        print('Stock: HYFM Index: NASDAQ')
        print(self.get_eps_info_test('HYFM'))
        
unit_test = Unit_Test()




