from email import header
from typing import Dict, List
from fundamental.mongo import MGDB
import pandas as pd
import os
from datetime import date
import json
import warnings
warnings.filterwarnings('ignore')
# This function print all the fundamental data and return a list
def print_newReq(symbol, dbname, colname):
    db = MGDB()
    Dic = db.get_symbol_dbinfo(symbol, dbname, colname)
    print("Exported fundamental data of " + str(symbol) + " sucessfully.")

    List = list()
    Basic_info = Dic['ProfileDict']
    cashFlow = Dic['CashFlowValue']
    scoreList = Dic['Score']
    Ratiodict = Dic['RatioDict']

    Epslist = Dic['EPSlist']
    EpsFormat = {
        'Date': None,
        'EPSGrowth': None,
        'EPSAcceleartion': None,
        'EPSSurpriseRTEstimated': None,
    }
    while len(Epslist) < 17:
        Epslist.append(EpsFormat)
    Incomelist = Dic['Incomelist']

    IncomeFormat = {
        'Date': None,
        'RevenueGrowth': None,
        'RevenueAcceleration': None,
        'ProfitMarginGrowth': None,
        'ProfitMarginAcceleration': None,
        'NetMarginGrowth': None,
        'NetMarginAcceleration': None,
    }

    while len(Incomelist) < 17:
        Incomelist.append(IncomeFormat)

    Pricechange = Dic['PriceChangeAfterReports']

    Volume_change = Dic['VolumeTrend']
    Major_holders = Dic['OverallInstHoldersDict']
    try:
        Major_list = ['% of Shares Held by All Insider', Major_holders['% of Shares Held by All Insider'],
                      '% of Shares Held by Institutions', Major_holders[
            '% of Shares Held by Institutions'],
            '% of Float Held by Institutions', Major_holders[
            '% of Float Held by Institutions'],
            'Number of Institutions Holding Shares', Major_holders['Number of Institutions Holding Shares']],
    except KeyError:
        Major_list = None
    Ins_holders = Dic['InstitutionHoldersList']
    InsList = list()
    for i in range(len(Ins_holders)):
        InsList.append(Ins_holders[i])

    Ins_holders = json.dumps(InsList, indent=4, sort_keys=True, default=str),

    Dict = {
        'STOCK': symbol,
        'Name:': Basic_info['name']if len(Basic_info) > 0 else None,
        'Sector:': Basic_info['sector']if len(Basic_info) > 0 else None,
        'Industry:': Basic_info['industry']if len(Basic_info) > 0 else None,
        'MarketCapitalization:': Basic_info['mktCap']if len(Basic_info) > 0 else None,
        'IpoDate:': Basic_info['ipoDate']if len(Basic_info) > 0 else None,
        'IpoAge:': Basic_info['ipoAge']if len(Basic_info) > 0 else None,
        'IsActivelyTrading:': Basic_info['activelyTrading']if len(Basic_info) > 0 else None,
        'Description:': Basic_info['description']if len(Basic_info) > 0 else None,
        'Country:': Basic_info['country']if len(Basic_info) > 0 else None,
        'Dcf-Time:': cashFlow['time']if len(cashFlow) > 0 else None,
        'Dcf:': cashFlow['dcf']if len(cashFlow) > 0 else None,
        'Price:': cashFlow['price']if len(cashFlow) > 0 else None,
        'altmanZScore:': scoreList['altmanZScore']if len(scoreList) > 0 else None,
        'piotroskiScore:': scoreList['piotroskiScore']if len(scoreList) > 0 else None,
        'MajorHolders:': Major_list,
        'InstitutionalHolders': Ins_holders,
        'RationlatestUpdateDate': Ratiodict['latestUpdateDate']if len(Ratiodict) > 0 else None,
        'Period': Ratiodict['period']if len(Ratiodict) > 0 else None,
        'returnOnCE': Ratiodict['returnOnCE']if len(Ratiodict) > 0 else None,
        'returnOnEquity': Ratiodict['returnOnEquity']if len(Ratiodict) > 0 else None,
        'priceToBookRatio': Ratiodict['priceToBookRatio']if len(Ratiodict) > 0 else None,
        'priceToSalesRatio': Ratiodict['priceToSalesRatio']if len(Ratiodict) > 0 else None,
        'priceFairValue': Ratiodict['priceFairValue']if len(Ratiodict) > 0 else None,
        'priceEarningsRatio': Ratiodict['priceEarningsRatio']if len(Ratiodict) > 0 else None,
        'debtRatio': Ratiodict['debtRatio']if len(Ratiodict) > 0 else None,

        '2022YearQuarter1Date:': Incomelist[0]['Date'] if len(Incomelist) > 0 else None,
        '2022YearQuarter1RevenueGrowth:': Incomelist[0]['RevenueGrowth'] if len(Incomelist) > 0 else None,
        '2022YearQuarter1RevenueAcceleration:': Incomelist[0]['RevenueAcceleration'] if len(Incomelist) > 0 else None,
        '2022YearQuarter1ProfitMarginGrowth:': Incomelist[0]['ProfitMarginGrowth'] if len(Incomelist) > 0 else None,
        '2022YearQuarter1ProfitMarginAcceleration:': Incomelist[0]['ProfitMarginAcceleration'] if len(Incomelist) > 0 else None,
        '2022YearQuarter1NetMarginGrowth:': Incomelist[0]['NetMarginGrowth'] if len(Incomelist) > 0 else None,
        '2022YearQuarter1NetMarginAcceleration:': Incomelist[0]['NetMarginAcceleration'] if len(Incomelist) > 0 else None,

        '2021YearQuarter4Date:': Incomelist[1]['Date'] if len(Incomelist) > 1 else None,
        '2021YearQuarter4RevenueGrowth:': Incomelist[1]['RevenueGrowth'] if len(Incomelist) > 1 else None,
        '2021YearQuarter4RevenueAcceleration:': Incomelist[1]['RevenueAcceleration'] if len(Incomelist) > 1 else None,
        '2021YearQuarter4ProfitMarginGrowth:': Incomelist[1]['ProfitMarginGrowth'] if len(Incomelist) > 1 else None,
        '2021YearQuarter4ProfitMarginAcceleration:': Incomelist[1]['ProfitMarginAcceleration'] if len(Incomelist) > 1 else None,
        '2021YearQuarter4NetMarginGrowth:': Incomelist[1]['NetMarginGrowth'] if len(Incomelist) > 1 else None,
        '2021YearQuarter4NetMarginAcceleration:': Incomelist[1]['NetMarginAcceleration'] if len(Incomelist) > 1 else None,

        '2021YearQuarter3Date:': Incomelist[2]['Date'] if len(Incomelist) > 2 else None,
        '2021YearQuarter3RevenueGrowth:': Incomelist[2]['RevenueGrowth']if len(Incomelist) > 2 else None,
        '2021YearQuarter3RevenueAcceleration:': Incomelist[2]['RevenueAcceleration']if len(Incomelist) > 2 else None,
        '2021YearQuarter3ProfitMarginGrowth:': Incomelist[2]['ProfitMarginGrowth']if len(Incomelist) > 2 else None,
        '2021YearQuarter3ProfitMarginAcceleration:': Incomelist[2]['ProfitMarginAcceleration']if len(Incomelist) > 2 else None,
        '2021YearQuarter3NetMarginGrowth:': Incomelist[2]['NetMarginGrowth']if len(Incomelist) > 2 else None,
        '2021YearQuarter3NetMarginAcceleration:': Incomelist[2]['NetMarginAcceleration']if len(Incomelist) > 2 else None,

        '2021YearQuarter2Date:': Incomelist[3]['Date']if len(Incomelist) > 3 else None,
        '2021YearQuarter2RevenueGrowth:': Incomelist[3]['RevenueGrowth']if len(Incomelist) > 3 else None,
        '2021YearQuarter2RevenueAcceleration:': Incomelist[3]['RevenueAcceleration']if len(Incomelist) > 3 else None,
        '2021YearQuarter2ProfitMarginGrowth:': Incomelist[3]['ProfitMarginGrowth']if len(Incomelist) > 3 else None,
        '2021YearQuarter2ProfitMarginAcceleration:': Incomelist[3]['ProfitMarginAcceleration']if len(Incomelist) > 3 else None,
        '2021YearQuarter2NetMarginGrowth:': Incomelist[3]['NetMarginGrowth']if len(Incomelist) > 3 else None,
        '2021YearQuarter2NetMarginAcceleration:': Incomelist[3]['NetMarginAcceleration']if len(Incomelist) > 3 else None,

        '2021YearQuarter1Date:': Incomelist[4]['Date']if len(Incomelist) > 4 else None,
        '2021YearQuarter1RevenueGrowth:': Incomelist[4]['RevenueGrowth']if len(Incomelist) > 4 else None,
        '2021YearQuarter1RevenueAcceleration:': Incomelist[4]['RevenueAcceleration']if len(Incomelist) > 4 else None,
        '2021YearQuarter1ProfitMarginGrowth:': Incomelist[4]['ProfitMarginGrowth']if len(Incomelist) > 4 else None,
        '2021YearQuarter1ProfitMarginAcceleration:': Incomelist[4]['ProfitMarginAcceleration']if len(Incomelist) > 4 else None,
        '2021YearQuarter1NetMarginGrowth:': Incomelist[4]['NetMarginGrowth']if len(Incomelist) > 4 else None,
        '2021YearQuarter1NetMarginAcceleration:': Incomelist[4]['NetMarginAcceleration']if len(Incomelist) > 4 else None,

        '2020YearQuarter4Date:': Incomelist[5]['Date']if len(Incomelist) > 5 else None,
        '2020YearQuarter4RevenueGrowth:': Incomelist[5]['RevenueGrowth']if len(Incomelist) > 5 else None,
        '2020YearQuarter4RevenueAcceleration:': Incomelist[5]['RevenueAcceleration']if len(Incomelist) > 5 else None,
        '2020YearQuarter4ProfitMarginGrowth:': Incomelist[5]['ProfitMarginGrowth']if len(Incomelist) > 5 else None,
        '2020YearQuarter4ProfitMarginAcceleration:': Incomelist[5]['ProfitMarginAcceleration']if len(Incomelist) > 5 else None,
        '2020YearQuarter4NetMarginGrowth:': Incomelist[5]['NetMarginGrowth']if len(Incomelist) > 5 else None,
        '2020YearQuarter4NetMarginAcceleration:': Incomelist[5]['NetMarginAcceleration']if len(Incomelist) > 5 else None,

        '2020YearQuarter3Date:': Incomelist[6]['Date']if len(Incomelist) > 7 else None,
        '2020YearQuarter3RevenueGrowth:': Incomelist[6]['RevenueGrowth']if len(Incomelist) > 6 else None,
        '2020YearQuarter3RevenueAcceleration:': Incomelist[6]['RevenueAcceleration']if len(Incomelist) > 6 else None,
        '2020YearQuarter3ProfitMarginGrowth:': Incomelist[6]['ProfitMarginGrowth']if len(Incomelist) > 6 else None,
        '2020YearQuarter3ProfitMarginAcceleration:': Incomelist[6]['ProfitMarginAcceleration']if len(Incomelist) > 6 else None,
        '2020YearQuarter3NetMarginGrowth:': Incomelist[6]['NetMarginGrowth']if len(Incomelist) > 6 else None,
        '2020YearQuarter3NetMarginAcceleration:': Incomelist[6]['NetMarginAcceleration']if len(Incomelist) > 6 else None,

        '2020YearQuarter2Date:': Incomelist[7]['Date']if len(Incomelist) > 7 else None,
        '2020YearQuarter2RevenueGrowth:': Incomelist[7]['RevenueGrowth']if len(Incomelist) > 7 else None,
        '2020YearQuarter2RevenueAcceleration:': Incomelist[7]['RevenueAcceleration']if len(Incomelist) > 7 else None,
        '2020YearQuarter2ProfitMarginGrowth:': Incomelist[7]['ProfitMarginGrowth']if len(Incomelist) > 7 else None,
        '2020YearQuarter2ProfitMarginAcceleration:': Incomelist[7]['ProfitMarginAcceleration']if len(Incomelist) > 7 else None,
        '2020YearQuarter2NetMarginGrowth:': Incomelist[7]['NetMarginGrowth']if len(Incomelist) > 7 else None,
        '2020YearQuarter2NetMarginAcceleration:': Incomelist[7]['NetMarginAcceleration']if len(Incomelist) > 7 else None,

        '2020YearQuarter1Date:': Incomelist[8]['Date']if len(Incomelist) > 8 else None,
        '2020YearQuarter1RevenueGrowth:': Incomelist[8]['RevenueGrowth']if len(Incomelist) > 8 else None,
        '2020YearQuarter1RevenueAcceleration:': Incomelist[8]['RevenueAcceleration']if len(Incomelist) > 8 else None,
        '2020YearQuarter1ProfitMarginGrowth:': Incomelist[8]['ProfitMarginGrowth']if len(Incomelist) > 8 else None,
        '2020YearQuarter1ProfitMarginAcceleration:': Incomelist[8]['ProfitMarginAcceleration']if len(Incomelist) > 8 else None,
        '2020YearQuarter1NetMarginGrowth:': Incomelist[8]['NetMarginGrowth']if len(Incomelist) > 8 else None,
        '2020YearQuarter1NetMarginAcceleration:': Incomelist[8]['NetMarginAcceleration']if len(Incomelist) > 8 else None,

        '2019YearQuarter4Date:': Incomelist[9]['Date']if len(Incomelist) > 9 else None,
        '2019YearQuarter4RevenueGrowth:': Incomelist[9]['RevenueGrowth']if len(Incomelist) > 9 else None,
        '2019YearQuarter4RevenueAcceleration:': Incomelist[9]['RevenueAcceleration']if len(Incomelist) > 9 else None,
        '2019YearQuarter4ProfitMarginGrowth:': Incomelist[9]['ProfitMarginGrowth']if len(Incomelist) > 9 else None,
        '2019YearQuarter4ProfitMarginAcceleration:': Incomelist[9]['ProfitMarginAcceleration']if len(Incomelist) > 9 else None,
        '2019YearQuarter4NetMarginGrowth:': Incomelist[9]['NetMarginGrowth']if len(Incomelist) > 9 else None,
        '2019YearQuarter4NetMarginAcceleration:': Incomelist[9]['NetMarginAcceleration']if len(Incomelist) > 9 else None,

        '2019YearQuarter3Date:': Incomelist[10]['Date']if len(Incomelist) > 10 else None,
        '2019YearQuarter3RevenueGrowth:': Incomelist[10]['RevenueGrowth']if len(Incomelist) > 10 else None,
        '2019YearQuarter3RevenueAcceleration:': Incomelist[10]['RevenueAcceleration']if len(Incomelist) > 10 else None,
        '2019YearQuarter3ProfitMarginGrowth:': Incomelist[10]['ProfitMarginGrowth']if len(Incomelist) > 10 else None,
        '2019YearQuarter3ProfitMarginAcceleration:': Incomelist[10]['ProfitMarginAcceleration']if len(Incomelist) > 10 else None,
        '2019YearQuarter3NetMarginGrowth:': Incomelist[10]['NetMarginGrowth']if len(Incomelist) > 10 else None,
        '2019YearQuarter3NetMarginAcceleration:': Incomelist[10]['NetMarginAcceleration']if len(Incomelist) > 10 else None,

        '2019YearQuarter2Date:': Incomelist[11]['Date']if len(Incomelist) > 11 else None,
        '2019YearQuarter2RevenueGrowth:': Incomelist[11]['RevenueGrowth']if len(Incomelist) > 11 else None,
        '2019YearQuarter2RevenueAcceleration:': Incomelist[11]['RevenueAcceleration']if len(Incomelist) > 11 else None,
        '2019YearQuarter2ProfitMarginGrowth:': Incomelist[11]['ProfitMarginGrowth']if len(Incomelist) > 11 else None,
        '2019YearQuarter2ProfitMarginAcceleration:': Incomelist[11]['ProfitMarginAcceleration']if len(Incomelist) > 11 else None,
        '2019YearQuarter2NetMarginGrowth:': Incomelist[11]['NetMarginGrowth']if len(Incomelist) > 11 else None,
        '2019YearQuarter2NetMarginAcceleration:': Incomelist[11]['NetMarginAcceleration']if len(Incomelist) > 11 else None,

        '2019YearQuarter1Date:': Incomelist[12]['Date']if len(Incomelist) > 12 else None,
        '2019YearQuarter1RevenueGrowth:': Incomelist[12]['RevenueGrowth']if len(Incomelist) > 12 else None,
        '2019YearQuarter1RevenueAcceleration:': Incomelist[12]['RevenueAcceleration']if len(Incomelist) > 12 else None,
        '2019YearQuarter1ProfitMarginGrowth:': Incomelist[12]['ProfitMarginGrowth']if len(Incomelist) > 12 else None,
        '2019YearQuarter1ProfitMarginAcceleration:': Incomelist[12]['ProfitMarginAcceleration']if len(Incomelist) > 12 else None,
        '2019YearQuarter1NetMarginGrowth:': Incomelist[12]['NetMarginGrowth']if len(Incomelist) > 12 else None,
        '2019YearQuarter1NetMarginAcceleration:': Incomelist[12]['NetMarginAcceleration']if len(Incomelist) > 12 else None,

        '2018YearQuarter4Date:': Incomelist[13]['Date']if len(Incomelist) > 13 else None,
        '2018YearQuarter4RevenueGrowth:': Incomelist[13]['RevenueGrowth']if len(Incomelist) > 13 else None,
        '2018YearQuarter4RevenueAcceleration:': Incomelist[13]['RevenueAcceleration']if len(Incomelist) > 13 else None,
        '2018YearQuarter4ProfitMarginGrowth:': Incomelist[13]['ProfitMarginGrowth']if len(Incomelist) > 13 else None,
        '2018YearQuarter4ProfitMarginAcceleration:': Incomelist[13]['ProfitMarginAcceleration']if len(Incomelist) > 13 else None,
        '2018YearQuarter4NetMarginGrowth:': Incomelist[13]['NetMarginGrowth']if len(Incomelist) > 13 else None,
        '2018YearQuarter4NetMarginAcceleration:': Incomelist[13]['NetMarginAcceleration']if len(Incomelist) > 13 else None,

        '2018YearQuarter3Date:': Incomelist[14]['Date']if len(Incomelist) > 14 else None,
        '2018YearQuarter3RevenueGrowth:': Incomelist[14]['RevenueGrowth']if len(Incomelist) > 14 else None,
        '2018YearQuarter3RevenueAcceleration:': Incomelist[14]['RevenueAcceleration']if len(Incomelist) > 14 else None,
        '2018YearQuarter3ProfitMarginGrowth:': Incomelist[14]['ProfitMarginGrowth']if len(Incomelist) > 14 else None,
        '2018YearQuarter3ProfitMarginAcceleration:': Incomelist[14]['ProfitMarginAcceleration']if len(Incomelist) > 14 else None,
        '2018YearQuarter3NetMarginGrowth:': Incomelist[14]['NetMarginGrowth']if len(Incomelist) > 14 else None,
        '2018YearQuarter3NetMarginAcceleration:': Incomelist[14]['NetMarginAcceleration']if len(Incomelist) > 14 else None,

        '2018YearQuarter2Date:': Incomelist[15]['Date']if len(Incomelist) > 15 else None,
        '2018YearQuarter2RevenueGrowth:': Incomelist[15]['RevenueGrowth']if len(Incomelist) > 15 else None,
        '2018YearQuarter2RevenueAcceleration:': Incomelist[15]['RevenueAcceleration']if len(Incomelist) > 15 else None,
        '2018YearQuarter2ProfitMarginGrowth:': Incomelist[15]['ProfitMarginGrowth']if len(Incomelist) > 15 else None,
        '2018YearQuarter2ProfitMarginAcceleration:': Incomelist[15]['ProfitMarginAcceleration']if len(Incomelist) > 15 else None,
        '2018YearQuarter2NetMarginGrowth:': Incomelist[15]['NetMarginGrowth']if len(Incomelist) > 15 else None,
        '2018YearQuarter2NetMarginAcceleration:': Incomelist[15]['NetMarginAcceleration']if len(Incomelist) > 15 else None,

        '2022YearQuarter1EPSDate:': Epslist[0]['Date']if len(Epslist) > 0 else None,
        '2022YearQuarter1EPSGrowth:': Epslist[0]['EPSGrowth']if len(Epslist) > 0 else None,
        '2022YearQuarter1EPSAcceleartion:': Epslist[0]['EPSAcceleartion']if len(Epslist) > 0 else None,
        '2022YearQuarter1EPSSurpriseRTEstimated:': Epslist[0]['EPSSurpriseRTEstimated']if len(Epslist) > 0 else None,

        '2021YearQuarter4EPSDate:': Epslist[1]['Date']if len(Epslist) > 1 else None,
        '2021YearQuarter4EPSGrowth:': Epslist[1]['EPSGrowth']if len(Epslist) > 1 else None,
        '2021YearQuarter4EPSAcceleartion:': Epslist[1]['EPSAcceleartion']if len(Epslist) > 1 else None,
        '2021YearQuarter4EPSSurpriseRTEstimated:': Epslist[1]['EPSSurpriseRTEstimated']if len(Epslist) > 1 else None,

        '2021YearQuarter3EPSDate:': Epslist[2]['Date']if len(Incomelist) > 2 else None,
        '2021YearQuarter3EPSGrowth:': Epslist[2]['EPSGrowth']if len(Incomelist) > 2 else None,
        '2021YearQuarter3EPSAcceleartion:': Epslist[2]['EPSAcceleartion']if len(Incomelist) > 2 else None,
        '2021YearQuarter3EPSSurpriseRTEstimated:': Epslist[2]['EPSSurpriseRTEstimated']if len(Incomelist) > 2 else None,

        '2021YearQuarter2EPSDate:': Epslist[3]['Date']if len(Epslist) > 3 else None,
        '2021YearQuarter2EPSGrowth:': Epslist[3]['EPSGrowth']if len(Epslist) > 3 else None,
        '2021YearQuarter2EPSAcceleartion:': Epslist[3]['EPSAcceleartion']if len(Epslist) > 3 else None,
        '2021YearQuarter2EPSSurpriseRTEstimated:': Epslist[3]['EPSSurpriseRTEstimated']if len(Epslist) > 3 else None,

        '2021YearQuarter1EPSDate:': Epslist[4]['Date']if len(Epslist) > 4 else None,
        '2021YearQuarter1EPSGrowth:': Epslist[4]['EPSGrowth']if len(Epslist) > 4 else None,
        '2021YearQuarter1EPSAcceleartion:': Epslist[4]['EPSAcceleartion']if len(Epslist) > 4 else None,
        '2021YearQuarter1EPSSurpriseRTEstimated:': Epslist[4]['EPSSurpriseRTEstimated']if len(Epslist) > 4 else None,

        '2020YearQuarter4EPSDate:': Epslist[5]['Date']if len(Epslist) > 5 else None,
        '2020YearQuarter4EPSGrowth:': Epslist[5]['EPSGrowth']if len(Epslist) > 5 else None,
        '2020YearQuarter4EPSAcceleartion:': Epslist[5]['EPSAcceleartion']if len(Epslist) > 5 else None,
        '2020YearQuarter4EPSSurpriseRTEstimated:': Epslist[5]['EPSSurpriseRTEstimated']if len(Epslist) > 5 else None,

        '2020YearQuarter3EPSDate:': Epslist[6]['Date']if len(Epslist) > 6 else None,
        '2020YearQuarter3EPSGrowth:': Epslist[6]['EPSGrowth']if len(Epslist) > 6 else None,
        '2020YearQuarter3EPSAcceleartion:': Epslist[6]['EPSAcceleartion']if len(Epslist) > 6 else None,
        '2020YearQuarter3EPSSurpriseRTEstimated:': Epslist[6]['EPSSurpriseRTEstimated']if len(Epslist) > 6 else None,

        '2020YearQuarter2EPSDate:': Epslist[7]['Date']if len(Epslist) > 7 else None,
        '2020YearQuarter2EPSGrowth:': Epslist[7]['EPSGrowth']if len(Epslist) > 7 else None,
        '2020YearQuarter2EPSAcceleartion:': Epslist[7]['EPSAcceleartion']if len(Epslist) > 7 else None,
        '2020YearQuarter2EPSSurpriseRTEstimated:': Epslist[7]['EPSSurpriseRTEstimated']if len(Epslist) > 7 else None,

        '2020YearQuarter1EPSDate:': Epslist[8]['Date']if len(Epslist) > 8 else None,
        '2020YearQuarter1EPSGrowth:': Epslist[8]['EPSGrowth']if len(Epslist) > 8 else None,
        '2020YearQuarter1EPSAcceleartion:': Epslist[8]['EPSAcceleartion']if len(Epslist) > 8 else None,
        '2020YearQuarter1EPSSurpriseRTEstimated:': Epslist[8]['EPSSurpriseRTEstimated']if len(Epslist) > 8 else None,

        '2019YearQuarter4EPSDate:': Epslist[9]['Date']if len(Epslist) > 9 else None,
        '2019YearQuarter4EPSGrowth:': Epslist[9]['EPSGrowth']if len(Epslist) > 9 else None,
        '2019YearQuarter4EPSAcceleartion:': Epslist[9]['EPSAcceleartion']if len(Epslist) > 9 else None,
        '2019YearQuarter4EPSSurpriseRTEstimated:': Epslist[9]['EPSSurpriseRTEstimated']if len(Epslist) > 9 else None,

        '2019YearQuarter3EPSDate:': Epslist[10]['Date']if len(Epslist) > 11 else None,
        '2019YearQuarter3EPSGrowth:': Epslist[10]['EPSGrowth']if len(Epslist) > 10 else None,
        '2019YearQuarter3EPSAcceleartion:': Epslist[10]['EPSAcceleartion']if len(Epslist) > 10 else None,
        '2019YearQuarter3EPSSurpriseRTEstimated:': Epslist[10]['EPSSurpriseRTEstimated']if len(Epslist) > 10 else None,

        '2019YearQuarter2EPSDate:': Epslist[11]['Date']if len(Epslist) > 11 else None,
        '2019YearQuarter2EPSGrowth:': Epslist[11]['EPSGrowth']if len(Epslist) > 11 else None,
        '2019YearQuarter2EPSAcceleartion:': Epslist[11]['EPSAcceleartion']if len(Epslist) > 11 else None,
        '2019YearQuarter23EPSSurpriseRTEstimated:': Epslist[11]['EPSSurpriseRTEstimated']if len(Epslist) > 11 else None,

        '2019YearQuarter1EPSDate:': Epslist[12]['Date']if len(Epslist) > 12 else None,
        '2019YearQuarter1EPSGrowth:': Epslist[12]['EPSGrowth']if len(Epslist) > 12 else None,
        '2019YearQuarter1EPSAcceleartion:': Epslist[12]['EPSAcceleartion']if len(Epslist) > 12 else None,
        '2019YearQuarter1EPSSurpriseRTEstimated:': Epslist[12]['EPSSurpriseRTEstimated']if len(Epslist) > 12 else None,

        '2018YearQuarter4EPSDate:': Epslist[13]['Date']if len(Epslist) > 13 else None,
        '2018YearQuarter4EPSGrowth:': Epslist[13]['EPSGrowth']if len(Epslist) > 13 else None,
        '2018YearQuarter4EPSAcceleartion:': Epslist[13]['EPSAcceleartion']if len(Epslist) > 13 else None,
        '2018YearQuarter4EPSSurpriseRTEstimated:': Epslist[13]['EPSSurpriseRTEstimated']if len(Epslist) > 13 else None,

        '2018YearQuarter3EPSDate:': Epslist[14]['Date']if len(Epslist) > 14 else None,
        '2018YearQuarter3EPSGrowth:': Epslist[14]['EPSGrowth']if len(Epslist) > 14 else None,
        '2018YearQuarter3EPSAcceleartion:': Epslist[14]['EPSAcceleartion']if len(Epslist) > 14 else None,
        '2018YearQuarter3EPSSurpriseRTEstimated:': Epslist[14]['EPSSurpriseRTEstimated']if len(Epslist) > 14 else None,

        '2018YearQuarter2EPSDate:': Epslist[15]['Date']if len(Epslist) > 15 else None,
        '2018YearQuarter2EPSGrowth:': Epslist[15]['EPSGrowth']if len(Epslist) > 15 else None,
        '2018YearQuarter2EPSAcceleartion:': Epslist[15]['EPSAcceleartion']if len(Epslist) > 15 else None,
        '2018YearQuarter2EPSSurpriseRTEstimated:': Epslist[15]['EPSSurpriseRTEstimated']if len(Epslist) > 15 else None,

        '2022YearQuarter1Price_Date:': Pricechange[0]['reported_date'] if len(Pricechange) > 0 else None,
        '2022YearQuarter1Price_day_1_change:': Pricechange[0]['day_1_change']if len(Pricechange) > 0 else None,
        '2022YearQuarter1Price_day_2_change:': Pricechange[0]['day_2_change']if len(Pricechange) > 0 else None,
        '2022YearQuarter1Price_day_4_change:': Pricechange[0]['day_4_change']if len(Pricechange) > 0 else None,
        '2022YearQuarter1Price_day_5_change:': Pricechange[0]['day_5_change']if len(Pricechange) > 0 else None,
        '2022YearQuarter1Price_day_10_change:': Pricechange[0]['day_10_change']if len(Pricechange) > 0 else None,
        '2022YearQuarter1Price_day_20_change:': Pricechange[0]['day_20_change']if len(Pricechange) > 0 else None,

        '2021YearQuarter4Price_Date:': Pricechange[1]['reported_date']if len(Pricechange) > 1 else None,
        '2021YearQuarter4Price_day_1_change:': Pricechange[1]['day_1_change']if len(Pricechange) > 1 else None,
        '2021YearQuarter4Price_day_2_change:': Pricechange[1]['day_2_change']if len(Pricechange) > 1 else None,
        '2021YearQuarter4Price_day_4_change:': Pricechange[1]['day_4_change']if len(Pricechange) > 1 else None,
        '2021YearQuarter4Price_day_5_change:': Pricechange[1]['day_5_change']if len(Pricechange) > 1 else None,
        '2021YearQuarter4Price_day_10_change:': Pricechange[1]['day_10_change']if len(Pricechange) > 1 else None,
        '2021YearQuarter4Price_day_20_change:': Pricechange[1]['day_20_change']if len(Pricechange) > 1 else None,

        '2021YearQuarter3Price_Date:': Pricechange[2]['reported_date']if len(Pricechange) > 2 else None,
        '2021YearQuarter3Price_day_1_change:': Pricechange[2]['day_1_change']if len(Pricechange) > 2 else None,
        '2021YearQuarter3Price_day_2_change:': Pricechange[2]['day_2_change']if len(Pricechange) > 2 else None,
        '2021YearQuarter3Price_day_4_change:': Pricechange[2]['day_4_change']if len(Pricechange) > 2 else None,
        '2021YearQuarter3Price_day_5_change:': Pricechange[2]['day_5_change']if len(Pricechange) > 2 else None,
        '2021YearQuarter3Price_day_10_change:': Pricechange[2]['day_10_change']if len(Pricechange) > 2 else None,
        '2021YearQuarter3Price_day_20_change:': Pricechange[2]['day_20_change']if len(Pricechange) > 2 else None,

        '2021YearQuarter2Price_Date:': Pricechange[3]['reported_date']if len(Pricechange) > 3 else None,
        '2021YearQuarter2Price_day_1_change:': Pricechange[3]['day_1_change']if len(Pricechange) > 3 else None,
        '2021YearQuarter2Price_day_2_change:': Pricechange[3]['day_2_change']if len(Pricechange) > 3 else None,
        '2021YearQuarter2Price_day_4_change:': Pricechange[3]['day_4_change']if len(Pricechange) > 3 else None,
        '2021YearQuarter2Price_day_5_change:': Pricechange[3]['day_5_change']if len(Pricechange) > 3 else None,
        '2021YearQuarter2Price_day_10_change:': Pricechange[3]['day_10_change']if len(Pricechange) > 3 else None,
        '2021YearQuarter2Price_day_20_change:': Pricechange[3]['day_20_change']if len(Pricechange) > 3 else None,

        '2021YearQuarter1Price_Date:': Pricechange[4]['reported_date']if len(Pricechange) > 4 else None,
        '2021YearQuarter1Price_day_1_change:': Pricechange[4]['day_1_change']if len(Pricechange) > 4 else None,
        '2021YearQuarter1Price_day_2_change:': Pricechange[4]['day_2_change']if len(Pricechange) > 4 else None,
        '2021YearQuarter1Price_day_4_change:': Pricechange[4]['day_4_change']if len(Pricechange) > 4 else None,
        '2021YearQuarter1Price_day_5_change:': Pricechange[4]['day_5_change']if len(Pricechange) > 4 else None,
        '2021YearQuarter1Price_day_10_change:': Pricechange[4]['day_10_change']if len(Pricechange) > 4 else None,
        '2021YearQuarter1Price_day_20_change:': Pricechange[4]['day_20_change']if len(Pricechange) > 4 else None,

        '2020YearQuarter4Price_Date:': Pricechange[5]['reported_date']if len(Pricechange) > 5 else None,
        '2020YearQuarter4Price_day_1_change:': Pricechange[5]['day_1_change']if len(Pricechange) > 5 else None,
        '2020YearQuarter4Price_day_2_change:': Pricechange[5]['day_2_change']if len(Pricechange) > 5 else None,
        '2020YearQuarter4Price_day_4_change:': Pricechange[5]['day_4_change']if len(Pricechange) > 5 else None,
        '2020YearQuarter4Price_day_5_change:': Pricechange[5]['day_5_change']if len(Pricechange) > 5 else None,
        '2020YearQuarter4Price_day_10_change:': Pricechange[5]['day_10_change']if len(Pricechange) > 5 else None,
        '2020YearQuarter4Price_day_20_change:': Pricechange[5]['day_20_change']if len(Pricechange) > 5 else None,

        '2020YearQuarter3Price_Date:': Pricechange[6]['reported_date']if len(Pricechange) > 6 else None,
        '2020YearQuarter3Price_day_1_change:': Pricechange[6]['day_1_change']if len(Pricechange) > 6 else None,
        '2020YearQuarter3Price_day_2_change:': Pricechange[6]['day_2_change']if len(Pricechange) > 6 else None,
        '2020YearQuarter3Price_day_4_change:': Pricechange[6]['day_4_change']if len(Pricechange) > 6 else None,
        '2020YearQuarter3Price_day_5_change:': Pricechange[6]['day_5_change']if len(Pricechange) > 6 else None,
        '2020YearQuarter3Price_day_10_change:': Pricechange[6]['day_10_change']if len(Pricechange) > 6 else None,
        '2020YearQuarter3Price_day_20_change:': Pricechange[6]['day_20_change']if len(Pricechange) > 6 else None,

        '2020YearQuarter2Price_Date:': Pricechange[7]['reported_date']if len(Pricechange) > 7 else None,
        '2020YearQuarter2Price_day_1_change:': Pricechange[7]['day_1_change']if len(Pricechange) > 7 else None,
        '2020YearQuarter2Price_day_2_change:': Pricechange[7]['day_2_change']if len(Pricechange) > 7 else None,
        '2020YearQuarter2Price_day_4_change:': Pricechange[7]['day_4_change']if len(Pricechange) > 7 else None,
        '2020YearQuarter2Price_day_5_change:': Pricechange[7]['day_5_change']if len(Pricechange) > 7 else None,
        '2020YearQuarter2Price_day_10_change:': Pricechange[7]['day_10_change']if len(Pricechange) > 7 else None,
        '2020YearQuarter2Price_day_20_change:': Pricechange[7]['day_20_change']if len(Pricechange) > 7 else None,

        '2020YearQuarter1Price_Date:': Pricechange[8]['reported_date']if len(Pricechange) > 8 else None,
        '2020YearQuarter1Price_day_1_change:': Pricechange[8]['day_1_change']if len(Pricechange) > 8 else None,
        '2020YearQuarter1Price_day_2_change:': Pricechange[8]['day_2_change']if len(Pricechange) > 8 else None,
        '2020YearQuarter1Price_day_4_change:': Pricechange[8]['day_4_change']if len(Pricechange) > 8 else None,
        '2020YearQuarter1Price_day_5_change:': Pricechange[8]['day_5_change']if len(Pricechange) > 8 else None,
        '2020YearQuarter1Price_day_10_change:': Pricechange[8]['day_10_change']if len(Pricechange) > 8 else None,
        '2020YearQuarter1Price_day_20_change:': Pricechange[8]['day_20_change']if len(Pricechange) > 8 else None,

        '2019YearQuarter4Price_Date:': Pricechange[9]['reported_date']if len(Pricechange) > 9 else None,
        '2019YearQuarter4Price_day_1_change:': Pricechange[9]['day_1_change']if len(Pricechange) > 9 else None,
        '2019YearQuarter4Price_day_2_change:': Pricechange[9]['day_2_change']if len(Pricechange) > 9 else None,
        '2019YearQuarter4Price_day_4_change:': Pricechange[9]['day_4_change']if len(Pricechange) > 9 else None,
        '2019YearQuarter4Price_day_5_change:': Pricechange[9]['day_5_change']if len(Pricechange) > 9 else None,
        '2019YearQuarter4Price_day_10_change:': Pricechange[9]['day_10_change']if len(Pricechange) > 9 else None,
        '2019YearQuarter4Price_day_20_change:': Pricechange[9]['day_20_change']if len(Pricechange) > 9 else None,

        '2019YearQuarter3Price_Date:': Pricechange[10]['reported_date']if len(Pricechange) > 10 else None,
        '2019YearQuarter3Price_day_1_change:': Pricechange[10]['day_1_change']if len(Pricechange) > 10 else None,
        '2019YearQuarter3Price_day_2_change:': Pricechange[10]['day_2_change']if len(Pricechange) > 10 else None,
        '2019YearQuarter3Price_day_4_change:': Pricechange[10]['day_4_change']if len(Pricechange) > 10 else None,
        '2019YearQuarter3Price_day_5_change:': Pricechange[10]['day_5_change']if len(Pricechange) > 10 else None,
        '2019YearQuarter3Price_day_10_change:': Pricechange[10]['day_10_change']if len(Pricechange) > 10 else None,
        '2019YearQuarter3Price_day_20_change:': Pricechange[10]['day_20_change']if len(Pricechange) > 10 else None,

        '2019YearQuarter2Price_Date:': Pricechange[11]['reported_date']if len(Pricechange) > 11 else None,
        '2019YearQuarter2Price_day_1_change:': Pricechange[11]['day_1_change']if len(Pricechange) > 11 else None,
        '2019YearQuarter2Price_day_2_change:': Pricechange[11]['day_2_change']if len(Pricechange) > 11 else None,
        '2019YearQuarter2Price_day_4_change:': Pricechange[11]['day_4_change']if len(Pricechange) > 11 else None,
        '2019YearQuarter2Price_day_5_change:': Pricechange[11]['day_5_change']if len(Pricechange) > 11 else None,
        '2019YearQuarter2Price_day_10_change:': Pricechange[11]['day_10_change']if len(Pricechange) > 11 else None,
        '2019YearQuarter2Price_day_20_change:': Pricechange[11]['day_20_change']if len(Pricechange) > 11 else None,

        '2019YearQuarter1Price_Date:': Pricechange[12]['reported_date']if len(Pricechange) > 12 else None,
        '2019YearQuarter1Price_day_1_change:': Pricechange[12]['day_1_change']if len(Pricechange) > 12 else None,
        '2019YearQuarter1Price_day_2_change:': Pricechange[12]['day_2_change']if len(Pricechange) > 12 else None,
        '2019YearQuarter1Price_day_4_change:': Pricechange[12]['day_4_change']if len(Pricechange) > 12 else None,
        '2019YearQuarter1Price_day_5_change:': Pricechange[12]['day_5_change']if len(Pricechange) > 12 else None,
        '2019YearQuarter1Price_day_10_change:': Pricechange[12]['day_10_change']if len(Pricechange) > 12 else None,
        '2019YearQuarter1Price_day_20_change:': Pricechange[12]['day_20_change']if len(Pricechange) > 12 else None,

        '2018YearQuarter4Price_Date:': Pricechange[13]['reported_date']if len(Pricechange) > 13 else None,
        '2018YearQuarter4Price_day_1_change:': Pricechange[13]['day_1_change']if len(Pricechange) > 13 else None,
        '2018YearQuarter4Price_day_2_change:': Pricechange[13]['day_2_change']if len(Pricechange) > 13 else None,
        '2018YearQuarter4Price_day_4_change:': Pricechange[13]['day_4_change']if len(Pricechange) > 13 else None,
        '2018YearQuarter4Price_day_5_change:': Pricechange[13]['day_5_change']if len(Pricechange) > 13 else None,
        '2018YearQuarter4Price_day_10_change:': Pricechange[13]['day_10_change']if len(Pricechange) > 13 else None,
        '2018YearQuarter4Price_day_20_change:': Pricechange[13]['day_20_change']if len(Pricechange) > 13 else None,

        '2018YearQuarter3Price_Date:': Pricechange[14]['reported_date']if len(Pricechange) > 14 else None,
        '2018YearQuarter3Price_day_1_change:': Pricechange[14]['day_1_change']if len(Pricechange) > 14 else None,
        '2018YearQuarter3Price_day_2_change:': Pricechange[14]['day_2_change']if len(Pricechange) > 14 else None,
        '2018YearQuarter3Price_day_4_change:': Pricechange[14]['day_4_change']if len(Pricechange) > 14 else None,
        '2018YearQuarter3Price_day_5_change:': Pricechange[14]['day_5_change']if len(Pricechange) > 14 else None,
        '2018YearQuarter3Price_day_10_change:': Pricechange[14]['day_10_change']if len(Pricechange) > 14 else None,
        '2018YearQuarter3Price_day_20_change:': Pricechange[14]['day_20_change']if len(Pricechange) > 14 else None,

        '2018YearQuarter2Price_Date:': Pricechange[15]['reported_date'] if len(Pricechange) > 15 else None,
        '2018YearQuarter2Price_day_1_change:': Pricechange[15]['day_1_change'] if len(Pricechange) > 15 else None,
        '2018YearQuarter2Price_day_2_change:': Pricechange[15]['day_2_change'] if len(Pricechange) > 15 else None,
        '2018YearQuarter2Price_day_4_change:': Pricechange[15]['day_4_change'] if len(Pricechange) > 15 else None,
        '2018YearQuarter2Price_day_5_change:': Pricechange[15]['day_5_change'] if len(Pricechange) > 15 else None,
        '2018YearQuarter2Price_day_10_change:': Pricechange[15]['day_10_change'] if len(Pricechange) > 15 else None,
        '2018YearQuarter2Price_day_20_change:': Pricechange[15]['day_20_change'] if len(Pricechange) > 15 else None,

        'Volume up days (10d)': Volume_change['VolumeUpDays(10d)'],
        'Volume up days (20d)': Volume_change['VolumeUpDays(20d)'],
        'Volume up days (50d)': Volume_change['VolumeUpDays(50d)'],
        'Volume up days (100d)': Volume_change['VolumeUpDays(100d)'],
        'Volume down days (10d)': Volume_change['VolumeDownDays(10d)'],
        'Volume down days (20d)': Volume_change['VolumeDownDays(20d)'],
        'Volume down days (50d)': Volume_change['VolumeDownDays(50d)'],
        'Volume down days (100d)': Volume_change['VolumeDownDays(100d)'],
        'Volume up/down ratio (10d)': Volume_change['Volumeup/downratio(10d)'],
        'Volume up/down ratio (20d)': Volume_change['Volumeup/downratio(20d)'],
        'Volume up/down ratio (50d)': Volume_change['Volumeup/downratio(50d)'],
        'Volume up/down ratio (100d)': Volume_change['Volumeup/downratio(100d)'],
    }
    List.append(Dict)
    return List

# this function read the symbols passed the conditions


def get_screened_symbols():

    symbols = []
    s = open("csv/symbols.txt", "r")

    for stock in s:
        symbols.append(stock.strip())

    s.close()
    return symbols

# this function is creating CSV file of fundamental data and save to a specifical folder


def get_fundamental():
    symbols = get_screened_symbols()
    result = pd.DataFrame()

    for symbol in symbols:
        info = print_newReq(symbol, 'superstockscreener', 'fundamentals_test')
        result = result.append(info)

    file_name = 'fundamental_data_' + \
        str(date.today()).replace('-', '') + '.csv'
    print("Fundamental data was exported and saved in --> " + file_name)

    result.to_csv(os.path.join('csv', file_name), index=False)
