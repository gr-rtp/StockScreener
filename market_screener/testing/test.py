from technical.stock_price_service import Stock_Price
from technical.index_price_service import Index_Price
from technical.data_pipeline import INITIAL_DATE, Data_Pipeline
from technical.technical_analysis import get_weighted_comp, get_dates, get_relative_strength
from technical.helpers import index_data, get_table_name
from time import perf_counter
import datetime
import pandas as pd
import concurrent.futures

# dates = get_dates(datetime.date.fromisoformat("2022-05-24"))

# for date in dates:
#     print(date)

def time_function(func):
    total = 0
    count = 0

    start_time = perf_counter()

    ###################################
    # perform all tasks to be timed here

    value = func()

    # end
    ###################################

    stop_time = perf_counter()
    diff = stop_time - start_time


    total += diff
    count += 1

    if diff > 60:
        print("Elapsed time to update stocks: " + str(diff / 60) + " minutes")
    elif diff > (60 * 60):
        print("Elapsed time to update stocks: " + str(diff / (60*60)) + " hours")
    else:
        print("Elapsed time to update stocks: " + str(diff) + " seconds")
    return value

def add_stocks(indexes, latest_date = INITIAL_DATE):

    for index in indexes:
        print('Starting ----------- ' + index + ' ----------- ')
        for stock in index_data[index]['components']:
            time_function(lambda: dp.load_stock_prices(stock, index, latest_date))
    
    print("\nTotal time: "  + str(total) + " seconds")
    print("\nAverage time: "  + str(total/count) + " seconds")

def update_stock_technicals(indexes, start_date = INITIAL_DATE):

    for index in indexes:
        print('Starting ----------- ' + index + ' ----------- ')
        for stock in index_data[index]['components']:
            symbol: str = stock

            if symbol.endswith(index_data[index]['suffix']):
                symbol = symbol.removesuffix(index_data[index]['suffix'])

            table_name = get_table_name(index, symbol)

            time_function(lambda: dp.load_stock_sma_volume(table_name, start_date))
    
    print("\nTotal time: "  + str(total) + " seconds")
    print("\nAverage time: "  + str(total/count) + " seconds")

def calc_weighted_comp(prices, latest_date = INITIAL_DATE):

    return time_function(lambda: get_weighted_comp(prices, latest_date))

def thread_me(name: str):
    return ("my name is " + name)

def test_get_dates():
    return time_function(lambda: get_dates(datetime.date.fromisoformat("2022-05-28"), 300))

def main():
    global total, count

    # initialise data pipeline with database access objects
    stock_price = Stock_Price()

    # datetime.date.fromisoformat("2022-05-09")

    # dp.update_stocks()

    # add_stocks(["DOW"], INITIAL_DATE)

    # update_stock_technicals(["DOW"], INITIAL_DATE)
    start_date = datetime.date.fromisoformat("2022-05-20")
    end_date = datetime.date.fromisoformat("2022-06-02")

    # vals = stock_price.get_prices_between_dates('sanbu_nasdaq', get_dates(start_date, 300)[3].astype(datetime.date), end_date, ['id', 'date', 'close'])

    # for val in vals:
    #     print(val)

    # print(pd.DataFrame(vals, columns=['id', 'date', 'close']).to_string())
    # return


    index_table_name = get_table_name("S&P500", "^GSPC")
    table_name = get_table_name("DOW", "AAPL")
    
    start_date = datetime.date.fromisoformat("2022-05-31")
    end_date = datetime.date.fromisoformat("2022-06-02")

    index_cum_prod = calc_weighted_comp(stock_price.get_prices_between_dates(index_table_name, get_dates(start_date, 300)[3].astype(datetime.date), end_date), start_date)
    stock_cum_prod = calc_weighted_comp(stock_price.get_prices_between_dates(table_name, get_dates(start_date, 300)[3].astype(datetime.date), end_date), start_date)

    # print(get_relative_strength(index_cum_prod, stock_cum_prod).to_string())

    

if __name__ == '__main__':
    main()