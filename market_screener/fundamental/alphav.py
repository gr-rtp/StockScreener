import requests
# import alpha_vantage
import yfinance as yf
import pandas as pd
from dotenv import dotenv_values
from config import ROOT_DIR
import os
config = dotenv_values(os.path.join(ROOT_DIR, 'db.local.env'))

# this function returns the EPS data and price change data in two lists.
def get_eps_info(symbol):
    api_url = "https://www.alphavantage.co/query"
    params = {
        "function": "EARNINGS",
        "symbol": symbol,
        "apikey": config['APH_KEY'],
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    price_change_list = list()
    # List stores all EPS info of single stock
    List = list()
    DateList = list()
    EPSGrowthList = list()
    EPSAccelerationList = list()
    EPSSurpriseRTEstimatedList = list()
    try:
        len(data['quarterlyEarnings'][0])
    except (KeyError, IndexError):
        return List, price_change_list

    if (len(data['quarterlyEarnings']) > 17):
        for num in range(0, 17):
            DateList.append(data['quarterlyEarnings'][num]['fiscalDateEnding'])
            try:
                EPSGrowthList.append((float(data['quarterlyEarnings'][num]['reportedEPS']) - float(data['quarterlyEarnings'][num+1]['reportedEPS'])) /
                                     float(data['quarterlyEarnings'][num+1]['reportedEPS']))
            except (ValueError, ZeroDivisionError):
                EPSGrowthList.append(None)
        for num in range(0, 16):
            try:
                if (EPSGrowthList[num + 1] == 0):
                    EPSAccelerationList.append(
                        (EPSGrowthList[num] - EPSGrowthList[num + 1]) / 0.01)
                else:
                    EPSAccelerationList.append(
                        (EPSGrowthList[num] - EPSGrowthList[num + 1]) / EPSGrowthList[num + 1])
            except TypeError:
                EPSAccelerationList.append(None)

            EPSSurpriseRTEstimatedList.append(
                data['quarterlyEarnings'][num]['surprisePercentage'])
            Dict = {'Date': DateList[num], 'EPSGrowth': EPSGrowthList[num], 'EPSAcceleartion': EPSAccelerationList[num],
                    'EPSSurpriseRTEstimated': EPSSurpriseRTEstimatedList[num]}
            List.append(Dict)
    else:
        for num in range(0, len(data['quarterlyEarnings'])-1):
            DateList.append(data['quarterlyEarnings'][num]['fiscalDateEnding'])
            try:
                EPSGrowthList.append((float(data['quarterlyEarnings'][num]['reportedEPS']) - float(data['quarterlyEarnings'][num+1]['reportedEPS'])) /
                                     float(data['quarterlyEarnings'][num+1]['reportedEPS']))
            except (ValueError, ZeroDivisionError):
                EPSGrowthList.append(None)
        for num in range(0, len(data['quarterlyEarnings'])-2):
            try:
                if(EPSGrowthList[num+1] == 0):
                    EPSAccelerationList.append(
                        (EPSGrowthList[num] - EPSGrowthList[num + 1]) / 0.01)
                else:
                    EPSAccelerationList.append(
                        (EPSGrowthList[num]-EPSGrowthList[num+1])/EPSGrowthList[num+1])
            except TypeError:
                EPSAccelerationList.append(None)

            EPSSurpriseRTEstimatedList.append(
                data['quarterlyEarnings'][num]['surprisePercentage'])
            Dict = {'Date': DateList[num], 'EPSGrowth': EPSGrowthList[num], 'EPSAcceleartion': EPSAccelerationList[num],
                    'EPSSurpriseRTEstimated': EPSSurpriseRTEstimatedList[num]}
            List.append(Dict)

    # create a list for price change data
    reported_date_list = list()
    day_1_change_list = list()
    day_2_change_list = list()
    day_4_change_list = list()
    day_5_change_list = list()
    day_10_change_list = list()
    day_20_change_list = list()

    ticker_object = yf.Ticker(symbol)
    df = ticker_object.history(period='5y')
    df = df.reset_index()

    try:
        reported_date_list.append(data['quarterlyEarnings'][0]['reportedDate'])
        index = df[df.Date == data['quarterlyEarnings'][0]['reportedDate']].index.tolist()[
            0]
        current_day_price = df.loc[index]['Close']

        if len(df) > index + 1:
            day_1_change_list.append(
                (df.loc[index+1]['Close']-current_day_price)/current_day_price)
        else:
            day_1_change_list.append(None)
        if len(df) > index + 2:
            day_2_change_list.append(
                (df.loc[index+2]['Close']-current_day_price)/current_day_price)
        else:
            day_2_change_list.append(None)
        if len(df) > index + 4:
            day_4_change_list.append(
                (df.loc[index + 4]['Close'] - current_day_price) / current_day_price)
        else:
            day_4_change_list.append(None)
        if len(df) > index + 5:
            day_5_change_list.append(
                (df.loc[index + 5]['Close'] - current_day_price) / current_day_price)
        else:
            day_5_change_list.append(None)
        if len(df) > index + 10:
            day_10_change_list.append(
                (df.loc[index + 10]['Close'] - current_day_price) / current_day_price)
        else:
            day_10_change_list.append(None)
        if len(df) > index + 20:
            day_20_change_list.append(
                (df.loc[index + 20]['Close'] - current_day_price) / current_day_price)
        else:
            day_20_change_list.append(None)
    except IndexError:
        day_1_change_list.append(None)
        day_2_change_list.append(None)
        day_4_change_list.append(None)
        day_5_change_list.append(None)
        day_10_change_list.append(None)
        day_20_change_list.append(None)

    Dict = {
        'reported_date': reported_date_list[0],
        'day_1_change': day_1_change_list[0],
        'day_2_change': day_2_change_list[0],
        'day_4_change': day_4_change_list[0],
        'day_5_change': day_5_change_list[0],
        'day_10_change': day_10_change_list[0],
        'day_20_change': day_20_change_list[0],
    }
    price_change_list.append(Dict)

    if len(data['quarterlyEarnings']) > 16:
        for num in range(1, 16):
            reported_date_list.append(
                data['quarterlyEarnings'][num]['reportedDate'])
            try:
                index = df[df.Date == data['quarterlyEarnings']
                           [num]['reportedDate']].index.tolist()[0]
            except:
                break
            current_day_price = df.loc[index]['Close']

            day_1_change_list.append(
                (df.loc[index + 1]['Close'] - current_day_price) / current_day_price)
            day_2_change_list.append(
                (df.loc[index + 2]['Close'] - current_day_price) / current_day_price)
            day_4_change_list.append(
                (df.loc[index + 4]['Close'] - current_day_price) / current_day_price)
            day_5_change_list.append(
                (df.loc[index + 5]['Close'] - current_day_price) / current_day_price)
            day_10_change_list.append(
                (df.loc[index + 10]['Close'] - current_day_price) / current_day_price)
            day_20_change_list.append(
                (df.loc[index + 20]['Close'] - current_day_price) / current_day_price)

            Dict = {
                'reported_date': reported_date_list[num],
                'day_1_change': day_1_change_list[num],
                'day_2_change': day_2_change_list[num],
                'day_4_change': day_4_change_list[num],
                'day_5_change': day_5_change_list[num],
                'day_10_change': day_10_change_list[num],
                'day_20_change': day_20_change_list[num],
            }
            price_change_list.append(Dict)

    else:
        for num in range(1, len(data['quarterlyEarnings'])):
            reported_date_list.append(
                data['quarterlyEarnings'][num]['reportedDate'])
            try:
                index = df[df.Date == data['quarterlyEarnings']
                           [num]['reportedDate']].index.tolist()[0]
            except:
                break
            current_day_price = df.loc[index]['Close']

            day_1_change_list.append(
                (df.loc[index + 1]['Close'] - current_day_price) / current_day_price)
            day_2_change_list.append(
                (df.loc[index + 2]['Close'] - current_day_price) / current_day_price)
            day_4_change_list.append(
                (df.loc[index + 4]['Close'] - current_day_price) / current_day_price)
            day_5_change_list.append(
                (df.loc[index + 5]['Close'] - current_day_price) / current_day_price)
            day_10_change_list.append(
                (df.loc[index + 10]['Close'] - current_day_price) / current_day_price)
            day_20_change_list.append(
                (df.loc[index + 20]['Close'] - current_day_price) / current_day_price)

            Dict = {
                'reported_date': reported_date_list[num],
                'day_1_change': day_1_change_list[num],
                'day_2_change': day_2_change_list[num],
                'day_4_change': day_4_change_list[num],
                'day_5_change': day_5_change_list[num],
                'day_10_change': day_10_change_list[num],
                'day_20_change': day_20_change_list[num],
            }
            price_change_list.append(Dict)
    return List, price_change_list

# this function returns a list contains quarterly Revenue, profit margin and net margin data.
def get_income_info(symbol):
    api_url = "https://www.alphavantage.co/query"
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": config['APH_KEY'],
    }

    response = requests.get(api_url, params=params)
    data = response.json()
    # List stores all Revenue and profit margin and net margin info of single stock
    List = list()
    DateList = list()

    RevenueGrowthList = list()
    RevenueAccelerationList = list()
    # RevenueSurpriseRTEstimatedList = list()

    ProfitMarginGrowthList = list()
    ProfitMarginAcList = list()

    NetMarginGrowthList = list()
    NetMarginAcList = list()

    try:
        len(data['quarterlyReports'])
    except KeyError:
        return List

    if (len(data['quarterlyReports']) > 17):
        for num in range(0, 17):
            DateList.append(data['quarterlyReports'][num]['fiscalDateEnding'])
            try:
                RevenueGrowthList.append((float(data['quarterlyReports'][num]['totalRevenue']) - float(data['quarterlyReports'][num + 1]['totalRevenue'])) /
                                         float(data['quarterlyReports'][num + 1]['totalRevenue']))
            except (ValueError, ZeroDivisionError):
                RevenueGrowthList.append(None)
            try:
                ProfitMarginGrowthList.append(((float(data['quarterlyReports'][num]['grossProfit']) / float(data['quarterlyReports'][num]['totalRevenue'])) -
                                               (float(data['quarterlyReports'][num + 1]['grossProfit']) / float(data['quarterlyReports'][num + 1]['totalRevenue']))) /
                                              (float(data['quarterlyReports'][num + 1]['grossProfit']) / float(data['quarterlyReports'][num + 1]['totalRevenue'])))
            except (ValueError, ZeroDivisionError):
                ProfitMarginGrowthList.append(None)
            try:
                NetMarginGrowthList.append((float(data['quarterlyReports'][num]['netIncome']) -
                                            float(data['quarterlyReports'][num + 1]['netIncome'])) /
                                           float(data['quarterlyReports'][num + 1]['netIncome']))
            except (ValueError, ZeroDivisionError):
                NetMarginGrowthList.append(None)

        for num in range(0, 16):
            try:
                if (RevenueGrowthList[num + 1] == 0):
                    RevenueAccelerationList.append(
                        (RevenueGrowthList[num] - RevenueGrowthList[num + 1]) / 0.01)
                else:
                    RevenueAccelerationList.append(
                        (RevenueGrowthList[num] - RevenueGrowthList[num + 1]) / RevenueGrowthList[num + 1])
            except TypeError:
                RevenueAccelerationList.append(None)
            try:
                if (ProfitMarginGrowthList[num + 1] == 0):
                    ProfitMarginAcList.append(
                        (ProfitMarginGrowthList[num] - ProfitMarginGrowthList[num + 1]) / 0.01)
                else:
                    ProfitMarginAcList.append(
                        (ProfitMarginGrowthList[num] - ProfitMarginGrowthList[num + 1]) / ProfitMarginGrowthList[
                            num + 1])
            except TypeError:
                ProfitMarginAcList.append(None)
            try:
                if (NetMarginGrowthList[num + 1] == 0):
                    NetMarginAcList.append(
                        (NetMarginGrowthList[num] - NetMarginGrowthList[num + 1]) / 0.01)
                else:
                    NetMarginAcList.append(
                        (NetMarginGrowthList[num] - NetMarginGrowthList[num + 1]) / NetMarginGrowthList[num + 1])
            except TypeError:
                NetMarginAcList.append(None)
            Dict = {'Date': DateList[num],
                    'RevenueGrowth': RevenueGrowthList[num],
                    'RevenueAcceleration': RevenueAccelerationList[num],
                    'ProfitMarginGrowth': ProfitMarginGrowthList[num],
                    'ProfitMarginAcceleration': ProfitMarginAcList[num],
                    'NetMarginGrowth': NetMarginGrowthList[num],
                    'NetMarginAcceleration': NetMarginAcList[num]}
            List.append(Dict)
    else:
        for num in range(0, len(data['quarterlyReports'])-1):
            DateList.append(data['quarterlyReports'][num]['fiscalDateEnding'])
            try:
                RevenueGrowthList.append((float(data['quarterlyReports'][num]['totalRevenue']) - float(data['quarterlyReports'][num+1]['totalRevenue'])) /
                                         float(data['quarterlyReports'][num+1]['totalRevenue']))
            except (ValueError, ZeroDivisionError):
                RevenueGrowthList.append(None)
            try:
                ProfitMarginGrowthList.append(((float(data['quarterlyReports'][num]['grossProfit'])/float(data['quarterlyReports'][num]['totalRevenue'])) -
                                               (float(data['quarterlyReports'][num+1]['grossProfit'])/float(data['quarterlyReports'][num+1]['totalRevenue']))) /
                                              (float(data['quarterlyReports'][num+1]['grossProfit'])/float(data['quarterlyReports'][num+1]['totalRevenue'])))
            except (ValueError, ZeroDivisionError):
                ProfitMarginGrowthList.append(None)
            try:
                NetMarginGrowthList.append((float(data['quarterlyReports'][num]['netIncome']) - float(data['quarterlyReports'][num+1]['netIncome'])) /
                                           float(data['quarterlyReports'][num+1]['netIncome']))
            except (ValueError, ZeroDivisionError):
                NetMarginGrowthList.append(None)

        for num in range(0, len(data['quarterlyReports'])-2):
            try:
                if(RevenueGrowthList[num+1] == 0):
                    RevenueAccelerationList.append(
                        (RevenueGrowthList[num] - RevenueGrowthList[num + 1]) / 0.01)
                else:
                    RevenueAccelerationList.append(
                        (RevenueGrowthList[num]-RevenueGrowthList[num+1])/RevenueGrowthList[num+1])
            except TypeError:
                RevenueAccelerationList.append(None)
            try:
                if(ProfitMarginGrowthList[num+1] == 0):
                    ProfitMarginAcList.append(
                        (ProfitMarginGrowthList[num]-ProfitMarginGrowthList[num+1])/0.01)
                else:
                    ProfitMarginAcList.append(
                        (ProfitMarginGrowthList[num] - ProfitMarginGrowthList[num + 1]) / ProfitMarginGrowthList[num + 1])
            except TypeError:
                ProfitMarginAcList.append(None)
            try:
                if(NetMarginGrowthList[num+1] == 0):
                    NetMarginAcList.append(
                        (NetMarginGrowthList[num]-NetMarginGrowthList[num+1])/0.01)
                else:
                    NetMarginAcList.append(
                        (NetMarginGrowthList[num] - NetMarginGrowthList[num + 1]) / NetMarginGrowthList[num + 1])
            except TypeError:
                NetMarginAcList.append(None)

            Dict = {'Date': DateList[num],
                    'RevenueGrowth': RevenueGrowthList[num],
                    'RevenueAcceleration': RevenueAccelerationList[num],
                    'ProfitMarginGrowth': ProfitMarginGrowthList[num],
                    'ProfitMarginAcceleration': ProfitMarginAcList[num],
                    'NetMarginGrowth': NetMarginGrowthList[num],
                    'NetMarginAcceleration': NetMarginAcList[num]}
            List.append(Dict)

    return List
