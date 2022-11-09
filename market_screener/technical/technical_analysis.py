from technical.stock_price_service import Stock_Price
from technical.helpers import holidays

import pandas as pd
import numpy as np

stock_price_service = Stock_Price()

def calc_price_average(prices: pd.DataFrame, windows = [50]):
    """
    Calculates the price moving average of a series of dates

    Parameters
    ----------
    prices : A dataframe containing at least two columns, a date column and a close (close price) column

    window : A list of numbers to be used as the number of datapoints required for each average,
    defaults to a list with the number 50 as it's only element
    """

    for window in windows:
        prices['sma' + str(window)] = prices['close'].rolling(window=window).mean().round(8)
    
    return prices



def calc_volume_average(prices: pd.DataFrame, windows = [50]):
    """
    Calculates the volume moving average of a series of dates

    Parameters
    ----------
    prices : A dataframe containing at least two columns, a date column and a volume column

    window : A list of numbers to be used as the number of datapoints required for each average,
    defaults to a list with the number 50 as it's only element
    """

    for window in windows:
        prices['volume' + str(window)] = prices['volume'].rolling(window=window).mean().round(8)
    
    return prices



def calc_sma_volume(historical_prices):
    """
    Calculate price moving averages and volume averages.
    Return values as a tuple containing tuples which each representing a row in the database

    Parameters
    ----------
    historical_prices : Must be a 2D tupple or list containing date, close and volume in each nested array
    """

    df = pd.DataFrame(historical_prices, columns=['date', 'close', 'volume'])

    calc_price_average(df, windows=[10, 50, 100, 150, 200])
    calc_volume_average(df, windows=[10, 50, 100, 150, 200])

    # df.fillna(0, inplace=True)
    df = df[df['volume200'].notna()]

    df.reset_index(inplace=True)
    df_to_np = df.to_numpy()

    tuple_list = []

    for x in df_to_np:
        temp_list = (x[1],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],)
        tuple_list.append(temp_list)

    return tuple_list



def get_high_low(historical_prices):
    """
    Iterate over prices and record the highest and lowest price within a 52 week period approximated as 240 days

    Parameters
    ----------
    historical_prices : Must be a 2D tupple or list containing date and close in each nested array
    """

    df = pd.DataFrame(historical_prices, columns=['date', 'high', 'low'])

    df['high_52_week'] = df['high'].rolling(window=240).max()
    df['low_52_week'] = df['low'].rolling(window=240).min()

    # df.fillna(0, inplace=True)
    df = df[df['high_52_week'].notna()]

    df.reset_index(inplace=True)
    df_to_np = df.to_numpy()

    tuple_list = []

    for x in df_to_np:
        temp_list = (x[1],x[4],x[5],)
        tuple_list.append(temp_list)

    return tuple_list



def get_dates(end_date, count):
    """
    Takes a target date as parameter and gets 4 evenly distributed earlier dates.
    In the case of a year, the 4 dates would be approximately 3 months of working days.
    For smaller periods, the dates will be evenly split into 4 quarters

    Parameters
    ----------
    end_date : Date from which to find the start 4 previous quarters
    count : maximum number of business days available to get dates from
    """

    max_period = -64

    # three_months = relativedelta(months=+3).days
    period = max(max_period, ((count // 4) * -1))

    #dates
    #last_3m
    end_last_3m = np.busday_offset(end_date, period, roll='backward', holidays=holidays)

    #second latest 3 months
    end_2nd_3m = np.busday_offset(end_last_3m, period, roll='backward', holidays=holidays)

    #third latest 3 months
    end_3rd_3m = np.busday_offset(end_2nd_3m, period, roll='backward', holidays=holidays)

    #forth latest 3 months
    end_4th_3m = np.busday_offset(end_3rd_3m, period, roll='backward', holidays=holidays)

    date_list = (
        end_last_3m,
        end_2nd_3m,
        end_3rd_3m,
        end_4th_3m,
        )

    return date_list



def get_weighted_comp(historical_prices, start_date, min_days = 8):
    """
    Calculate the cummulative product for a given symbol and a date from which the cummulative product is required.
    This calculation is weighed 40% for most recent quarter and 20% for the remaining three quarters
    """

    df = pd.DataFrame(historical_prices, columns=['date', 'close'])

    if df.empty:
        return df

    df['Weighted_comp'] = np.NaN
    df['change'] = df['close'].astype(float).pct_change().add(1)

    min_date = df['date'].iloc[0]

    i = 0

    for index, row in df.iterrows():
        i += 1

        if row['date'] >= start_date and i > min_days:
            date = get_dates(row['date'], i - 1)

            req_date = date[3]
            results = [0, 0, 0, 0]

            if min_date <= req_date:


                try:
                    #last 3 months
                    results[0] = df[(df['date'] > (date[0])) & (df['date'] <= row['date'])]['change'].cumprod().iat[-1]
                    results[1] = df[(df['date'] > (date[1])) & (df['date'] <= date[0])]['change'].cumprod().iat[-1]
                    results[2] = df[(df['date'] > (date[2])) & (df['date'] <= date[1])]['change'].cumprod().iat[-1]
                    results[3] = df[(df['date'] > (date[3])) & (df['date'] <= date[2])]['change'].cumprod().iat[-1]

                    df.at[index, 'Weighted_comp'] = (0.4 * results[0]) + (0.2 * results[1]) + (0.2 * results[2]) + (0.2 * results[3])
                except :
                    continue
    return df[df['Weighted_comp'].notna()][['date','Weighted_comp']]



def get_relative_strength(index_cum_prod, stock_cum_prod: pd.DataFrame):
    """
    Takes the cummulative products of an index over a period and the cummulative products of a stock over a period
    Joins the cummulative periods based on dates that match and divides the stock values by index values.
    The result is converted to a list of tuples each containing date and relative strength for each date
    """
    stock_cum_prod = stock_cum_prod.merge(index_cum_prod, 'inner', 'date')

    stock_cum_prod['relative strength'] = stock_cum_prod['Weighted_comp_x'] / stock_cum_prod['Weighted_comp_y']

    stock_cum_prod = stock_cum_prod[stock_cum_prod['relative strength'].notna()][["date", "relative strength"]]

    stock_cum_prod.reset_index(inplace=True)
    df_to_np = stock_cum_prod.to_numpy()

    tuple_list = []

    for x in df_to_np:
        temp_list = (x[1],x[2],)
        tuple_list.append(temp_list)

    return tuple_list