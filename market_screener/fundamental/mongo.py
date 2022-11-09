import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
from config import ROOT_DIR
import os

import fundamental.alphav as alphav
import fundamental.fmp as fmp
import fundamental.yahoo as yahoo
import fundamental.yahoofin as yahoofin

import time

config = dotenv_values(os.path.join(ROOT_DIR, 'db.local.env'))


class MGDB:
    # Create a database object
    def __init__(self):
        self.client = pymongo.MongoClient(config['MGDB_HOST'])
        # conn_str = "mongodb+srv://Grayson:212002@cluster0.aicuq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        # self.client = pymongo.MongoClient(conn_str, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
        
    # gathering all fundamental data and return a dictionary
    def create_symbol_dbinfo(self,symbol):

        epslist,priceafterreportlist = alphav.get_eps_info(symbol)
        incomelist = alphav.get_income_info(symbol)
        ratiodict = fmp.get_ratios_info(symbol)
        profiledict = fmp.get_profile_info(symbol)
        scoredict = fmp.get_score(symbol)
        cashflowdict = fmp.get_cashFlowvalue(symbol)
        insholder = yahoo.get_inst_info(symbol)
        overallinstdict = yahoo.get_major_holders(symbol)
        volumetrenddict = yahoo.get_volume_change(symbol)


        Dict = {'Symbol': symbol,
                'EPSlist': epslist,
                'Incomelist': incomelist,
                'RatioDict': ratiodict,
                'ProfileDict': profiledict,
                'InstitutionHoldersList': insholder,
                'OverallInstHoldersDict': overallinstdict,
                'VolumeTrend': volumetrenddict,
                'PriceChangeAfterReports': priceafterreportlist,
                'Score': scoredict,
                'CashFlowValue': cashflowdict
                }
        return Dict

    # insert one symbol with data to database
    def insert_symbol(self,dbname, colname, fdDict):

        mydb = self.client[dbname]
        mycol = mydb[colname]
        x = mycol.insert_one(fdDict)

        print(str(x.inserted_id)+": "+fdDict['Symbol']+" added")

    # insert multiple symbols with data to database
    def insert_multiple_symbols(self,dbname, colname, symbols):
        for symbol in symbols:
            dbSymbolinfo = self.create_symbol_dbinfo(symbol)
            time.sleep(35)
            self.insert_symbol(dbname, colname, dbSymbolinfo)

    # insert, detelete, update symbols based on the new dataset
    def daily_update(self,dbname, colname, symbols):
        mydb = self.client[dbname]
        mycol = mydb[colname]
        dbsymbols = list()
        for i in mycol.find({}, {"Symbol": 1}):
            dbsymbols.append(i['Symbol'])

        existedSymbols = list()
        waitforDSymbols = list()
        newSymbols = list()

        # for symbols in DB and also in the new list, leave them
        # for symbols in DB but not in the new list, delete them
        for x in dbsymbols:
            if x in symbols:
                existedSymbols.append(x)
            else:
                waitforDSymbols.append(x)

        # for symbols in the new list but not in DB, add them
        for y in symbols:
            if y not in dbsymbols:
                newSymbols.append(y)

        print("#### Starting to update fundamental data ... ####")
        print("Stocks in the database")
        print(dbsymbols)
        print("New stocks that are already in the database: ")
        print(existedSymbols)
        print("Old stocks to be deleted: ")
        print(waitforDSymbols)
        print("New stocks to be added: ")
        print(newSymbols)

        # for z in waitforDSymbols:
        #     mycol.delete_one({"Symbol": z})
        #     print(z+" deleted")

        self.insert_multiple_symbols(dbname, colname, newSymbols)

        for j in existedSymbols:
            ratios = fmp.get_ratios_info(j)
            profile = fmp.get_profile_info(j)
            volumetrend = yahoo.get_volume_change(j)

            myquery = {"Symbol": j}
            newvalues = {"$set": {"RatioDict": ratios,"ProfileDict": profile,"VolumeTrend": volumetrend}}

            mycol.update_one(myquery, newvalues)
            print(j+" updated")

    # extract all fundamental data of one symbol
    def get_symbol_dbinfo(self, symbol, dbname, colname):
        mydb = self.client[dbname]
        mycol = mydb[colname]
        myquery = {"Symbol": symbol}
        for x in mycol.find(myquery):
            return x


    # update all database every week
    # def weekly_update(self)


mongo = MGDB()