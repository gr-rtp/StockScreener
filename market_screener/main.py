from technical.data_pipeline import data_pipeline as dp
from technical.screener import screener
from technical.helpers import available_indexes
from fundamental.print_data import get_fundamental, get_screened_symbols
from testing.unittest import unit_test as ut
from fundamental.mongo import mongo

import click_spinner
import datetime
import fire

import concurrent.futures
import os

from dotenv import dotenv_values

config = dotenv_values('db.local.env')


def pretty_print_list(list):
    for x in list:
        print(x)


# takes a function and a list of arguments
# calls the function once for each argument
def use_multiprocessing(func, args):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(func, args)


def update_stocks(index):
    dp.update_stocks_of_index(index)


def daily_update():
    """
    Updates all stocks in the database from their last date of price data to the most
    recently closed date.
    Also calculates technical indicators such as relative strength used to rank stocks.
    Performs a screening based on rank and returns a daily dataset of all stocks ranked against the S&P500 index
    Passes screened results to fundamental analysis and retrieves fundamental data for screened stocks.
    """
    # first of all update all stocks and index price tables
    # from their last date to the most recently closed date
    use_multiprocessing(update_stocks, available_indexes)

    # next, we update the sp500 relative strengths on all stock tables
    use_multiprocessing(update_sp500_rs, available_indexes)

    # then, we prepare the daily datasets for each index
    dp.index_price_service.prepare_dataset(dp.yesterday.isoformat(), 'DOW')
    dp.index_price_service.prepare_dataset(dp.yesterday.isoformat(), 'S&P500')
    dp.index_price_service.prepare_dataset(dp.yesterday.isoformat(), 'NYSE')
    dp.index_price_service.prepare_dataset(dp.yesterday.isoformat(), 'NASDAQ')

    dp.index_price_service.prepare_dataset(dp.yesterday.isoformat(), 'S&P500', [
                                           'DOW', 'S&P500', 'NYSE', 'NASDAQ'])

    # # finally, we prepare a daily dataset for all stocks against the sp500
    get_sp500_dataset(dp.yesterday.isoformat())
    # get_dataset('2022-06-01')

    # ################### fundamental functions called ###################

    # update mongDB
    mongo.daily_update('superstockscreener', 'fundamentals_test',
                       get_screened_symbols())

    # print fundamental data
    get_fundamental()

    return


def custom_update(index, rs_start=dp.yesterday.isoformat(), rs_end=dp.yesterday.isoformat()):
    """
    Updates prices of all stocks in the specified index until last trading day and update relative strength of period of specified start and end dates.

    Note: dates are only used to specify the period to update relative strength

    Examples:
    python main.py get_custom_update "'S&P500'" 2022-06-10 2022-06-10 (update price data until last trading day and update relative strength only on 2022-06-10)
    python main.py get_custom_update ""DOW"" 2022-05-27 2022-06-10 (update price data until last trading day and update relative strength only from 2022-05-27 to 2022-06-10)

    Parameters
    ---------
    index: Specify the index for which you would like to update all stocks. The index should be in string format (i.e. "'NASDAQ'")
    rs_start: Update the relative strength for the specified index against the S&P500 index starting from this date. Date should be in ISO format (i.e. 2022-05-15)
    rs_end: Update the relative strength for the specified index against the S&P500 index ending on this date. Date should be in ISO format (i.e. 2022-05-27)
    """

    # convert start and end dates into datetime.date
    rs_end_date = datetime.date.fromisoformat(rs_end)
    rs_start_date = datetime.date.fromisoformat(rs_start)

    update_stocks(index)

    dp.update_own_relative_strength(index, rs_start_date, rs_end_date)

    # next, we update the sp500 relative strengths on all stock tables
    dp.update_reference_relative_strength(
        "S&P500", index, 'relative_strength_sp500', rs_start_date, rs_end_date)

    # then, we prepare the daily datasets for each index
    dp.index_price_service.prepare_dataset(rs_end, index)

    # # finally, we prepare a daily dataset for all stocks against the sp500
    get_index_dataset(index, rs_end)
    return


def update_sp500_rs(index):
    dp.update_reference_relative_strength(
        "S&P500", index, 'relative_strength_sp500', datetime.date.fromisoformat('2022-06-04'))


def get_index_dataset(index: str, date: str):
    """
    Prepared a dataset containing all stocks in the specified index at the specified date.
    Stocks are ranked by relative strength (relative to specified index).

    Please update the price and relative strengths of the index on the specified date before attempting to get a dataset with this function.

    Examples:
    python main.py get_index_dataset "'S&P500'" 2022-05-27
    python main.py get_index_dataset --index="'S&P500'" --date=2022-05-27

    Parameters
    ---------
    :param index: Specify the index for which you would like to prepare and screen a dataset. The index should be in string format (i.e. "'NASDAQ'")
    :param date: The date you are interested in ranking for. Date should be in ISO format (i.e. 2022-05-15)
    """

    dp.index_price_service.prepare_dataset(date, index)

    results = screener.screen_self(index, date, columns=[
                                   'symbol', 'close', 'volume', 'relative_strength_sp500', 'rank'])

    symbols_list = results['symbol'].tolist()

    with open('csv/' + index.lower() + '_symbols.txt', 'w') as f:
        for item in symbols_list:
            f.write("%s\n" % item)

        f.close()

    # print(results.to_string())

    file_name = index.lower() + '_dataset_' + date.replace('-', '') + '.csv'
    print("A copy of the results were saved to --> " + file_name)

    results.to_csv(os.path.join('csv', file_name))


def get_sp500_dataset(date: str):
    """
    Prepared a dataset containing all stocks from ALL INDEXES at the specified date.
    Stocks are ranked by relative strength (relative to S&P500).

    Please update the price and relative strengths of the index on the specified date before attempting to get a dataset with this function.

    Examples:
    python main.py get_sp500_dataset 2022-12-22
    python main.py get_sp500_dataset --date=2010-06-24

    Parameters
    ---------
    :param date: The date you are interested in ranking for. Date should be in ISO format (i.e. 2022-05-15)
    """

    conditions = ["close > sma150", "close > sma200", "sma150 > sma200", "sma50 > sma150",
                  "close > sma50", "close >= (1.3*low_52_week)", "close >= (0.75*high_52_week)"]

    dp.index_price_service.prepare_dataset(
        date, 'S&P500', ['DOW', 'S&P500', 'NYSE', 'NASDAQ'])

    results = screener.screen_against_reference('S&P500', date, conditions, [
                                                'symbol', 'open', 'close', 'high', 'low', 'volume', 'relative_strength', 'relative_strength_sp500', 'rank'])

    symbols_list = results['symbol'].tolist()

    with open('csv/symbols.txt', 'w') as f:
        for item in symbols_list:
            f.write("%s\n" % item)

        f.close()

    # print(results.to_string())

    file_name = 'sp500_daily_dataset_' + date.replace('-', '') + '.csv'
    print("A copy of the results were saved to --> " + file_name)

    results.to_csv(os.path.join('csv', file_name))


def screen_dataset(index, date, conditions=[]):
    """
    Screen already prepared datasets to further filter stocks accorgding to your strategy

    Note: daily_dataset of the same date should be created (using get_index_dataset command) before running this command.

    Examples:
    python main.py screen_dataset "'S&P500'" 2022-05-27
    python main.py screen_dataset --index="'S&P500'" --date=2022-05-27

    python main.py screen_dataset "'DOW'" 2022-05-27 "'["open > close", "sma10 > sma50"]'"
    python main.py screen_dataset --index="'DOW'" --date=2022-05-27 --conditions='["open > close", "sma10 > sma50"]'

    Parameters
    ---------
    :param index: The index dataset you are interested in screening. The index should be in string format (i.e. "'NASDAQ'")
    :param date: The date you are interested in ranking for. Date should be in ISO format (i.e. 2022-05-15)
    :param conditions: List (Array) of SQL conditions to filter with as strings e.g. '["open > close", "sma10 > sma50"]' wrap the list in single quotes to ensure it is parsed properly.
    """
    results = screener.screen_self(index, date, conditions, columns=[
                                   'symbol', 'open', 'close', 'high', 'low', 'volume', 'relative_strength', 'relative_strength_sp500', 'rank'])

    symbols_list = results['symbol'].tolist()

    with open('csv/' + index.lower() + '_symbols.txt', 'w') as f:
        for item in symbols_list:
            f.write("%s\n" % item)

        f.close()

    # print(results.to_string())

    file_name = index.lower() + '_dataset_' + date.replace('-', '') + '.csv'
    print("A copy of the results were saved to --> " + file_name)

    results.to_csv(os.path.join('csv', file_name))
    return


def screen_sp500_dataset(date, conditions=[]):
    """
    Screen already prepared datasets to further filter stocks accorgding to your strategy.
    Specifically dataset for stocks ranked against S&P500 on the specified date.

    Note: daily_dataset of the same date should be created (using get_sp500_dataset command) before running this command.

    Examples:
    python main.py screen_dataset 2022-05-27
    python main.py screen_dataset --date=2022-05-27

    python main.py screen_dataset 2022-05-27 '["open > close", "sma10 > sma50"]'
    python main.py screen_dataset --index="'DOW'" --date=2022-05-27 --conditions='["open > close", "sma10 > sma50"]'

    Parameters
    ---------
    :param date: The date you are interested in ranking for. Date should be in ISO format (i.e. 2022-05-15)
    :param conditions: List (Array) of SQL conditions to filter with as strings e.g. '["open > close", "sma10 > sma50"]' wrap the list in single quotes to ensure it is parsed properly.
    """

    results = screener.screen_against_reference('S&P500', date, conditions, [
                                                'symbol', 'open', 'close', 'high', 'low', 'volume', 'relative_strength', 'relative_strength_sp500', 'rank'])

    symbols_list = results['symbol'].tolist()

    with open('csv/symbols.txt', 'w') as f:
        for item in symbols_list:
            f.write("%s\n" % item)

        f.close()

    # print(results.to_string())

    file_name = 'sp500_daily_dataset_' + date.replace('-', '') + '.csv'
    print("A copy of the results were saved to --> " + file_name)

    results.to_csv(os.path.join('csv', file_name))
    return


def show_stats():
    """
    Shows the status of database and performs tests to check data quality
    """
    with click_spinner.spinner():
        print(dp.get_total_dates())
        print(dp.get_total_stocks())
        # ut.execute_unittests().v


if __name__ == "__main__":
    fire.Fire({
        "update_all": daily_update,
        "update": custom_update,
        "get_dataset": get_index_dataset,
        "get_dataset_sp500": get_sp500_dataset,
        "screen_dataset": screen_dataset,
        "screen_dataset_sp500": screen_sp500_dataset,
        "status": show_stats
    })
