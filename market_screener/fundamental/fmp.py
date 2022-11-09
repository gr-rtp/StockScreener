#!/usr/bin/env python
import requests
import pandas as pd
import datetime
import certifi
import json
from dotenv import dotenv_values
from config import ROOT_DIR
import os
config = dotenv_values(os.path.join(ROOT_DIR, 'db.local.env'))

# this function returns all the ration data of stock

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    result = requests.get(url).json()
    return result


def get_ratios_info(symbol):
    url = 'https://financialmodelingprep.com/api/v3/ratios/' + \
        symbol + '?apikey=' + config['FMP_KEY']
    data = get_jsonparsed_data(url)
    if len(data) == 0:
        return dict()

    try:
        latestUpdateDate = data[0]['date']
        returnOnCE = data[0]['returnOnCapitalEmployed']
        returnOnEquity = data[0]['returnOnEquity']
        priceToBookRatio = data[0]['priceToBookRatio']
        priceToSalesRatio = data[0]['priceToSalesRatio']
        priceFairValue = data[0]['priceFairValue']
        priceEarningsRatio = data[0]['priceEarningsRatio']
        debtRatio = data[0]['debtRatio']
    except KeyError:
        latestUpdateDate = None
        returnOnCE = None
        returnOnEquity = None
        priceToBookRatio = None
        priceToSalesRatio = None
        priceFairValue = None
        priceEarningsRatio = None
        debtRatio = None

    Dict = {'symbol': symbol,
            'latestUpdateDate': latestUpdateDate,
            'period': 'OneYear',
            'returnOnCE': returnOnCE,
            'returnOnEquity': returnOnEquity,
            'priceToBookRatio': priceToBookRatio,
            'priceToSalesRatio': priceToSalesRatio,
            'priceFairValue': priceFairValue,
            'priceEarningsRatio': priceEarningsRatio,
            'debtRatio': debtRatio}
    return Dict

# this function returns all the basic info of stock


def get_profile_info(symbol):
    url = 'https://financialmodelingprep.com/api/v3/profile/' + \
        symbol+'?apikey=' + config['FMP_KEY']
    data = get_jsonparsed_data(url)

    if len(data) == 0:
        return dict()

    try:
        name = data[0]['companyName']
    except KeyError:
        name = None
    industry = data[0]['industry']
    sector = data[0]['sector']
    mktCap = data[0]['mktCap']
    ipoDate = data[0]['ipoDate']
    try:
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        ipo_year = year - int(float(ipoDate[0:4]))
        ipo_month = round(month - int(float(ipoDate[5:7])), 2)
        ipoAge = ipo_year+(ipo_month/12)
    except ValueError:
        ipoAge = None
    ActivelyTrading = data[0]['isActivelyTrading']
    Description = data[0]['description']
    Country = data[0]['country']

    Dict = {
        'name': name,
        'industry': industry,
        'sector': sector,
        'symbol': symbol,
        'ipoDate': ipoDate,
        'mktCap': mktCap,
        'ipoAge': ipoAge,
        'activelyTrading': ActivelyTrading,
        'description': Description,
        'country': Country,

    }
    return Dict

# this function returns the altmanZScore and piotroskiScore


def get_score(symbol):
    url = "https://financialmodelingprep.com/api/v4/score?symbol=" + \
          symbol + "&apikey=" + config['FMP_KEY']
    data = get_jsonparsed_data(url)
    if len(data) == 0:
        altmanZScore = None
    else:
        altmanZScore = data[0]['altmanZScore']

    if len(data) == 0:
        piotroskiScore = None
    else:
        piotroskiScore = data[0]['piotroskiScore']
    Dict = {
        'altmanZScore': altmanZScore,
        'piotroskiScore': piotroskiScore
    }
    return Dict

# this function returns the data related to the stock dcf value


def get_cashFlowvalue(symbol):
    url = 'https://financialmodelingprep.com/api/v3/discounted-cash-flow/' + \
          symbol + '?apikey=' + config['FMP_KEY']
    data = get_jsonparsed_data(url)
    if len(data) == 0:
        return dict()
    try:
        date = data[0]['date']
    except KeyError:
        date = None
    try:
        dcf_value = data[0]['dcf']
    except KeyError:
        dcf_value = None
    try:
        price = data[0]['Stock Price']
    except:
        price = None
    Dict = {
        'time': date,
        'dcf': dcf_value,
        'price': price
    }
    return Dict
