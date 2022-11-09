from yahoo_fin import stock_info as sf
import numpy as np
import datetime

iterations = {
    "DOW": 1,
    "S&P500": 1,
    "NYSE": 2,
    "NASDAQ": 3
}

def nyse_to_array ():
    symbols = []

    f = open("technical/nyse_symbols_13052022.txt", "r")

    for stock in f:
        symbol = stock.split("\t")[0]
        if "^" in symbol or "/" in symbol:
            continue
        # symbol = symbol.replace("^", "-P")
        # symbol = symbol.replace("/", "-")

        symbols.append(symbol)

    f.close()
    # print("NYSE stock count: " + str(len(symbols)))

    return symbols

# print(data)
available_indexes = [
    "DOW",
    "S&P500",
    "NYSE",
    "NASDAQ",
    # "FTSE100",
    # "FTSE250",
    # "IBOVESPA",
    # "NIFTY50",
    # "NIFTYBANK"
]

major_indexes = [
    # "DOW",
     "S&P500",
    # "NYSE",
    # "NASDAQ",
]

index_data = {
    "NYSE": {
        "name": "New York Stock Exchange Composite",
        "country": "Unites States",
        "components": nyse_to_array(),
        "suffix": "",
        "symbol": "^NYA"
    },
    "DOW": {
        "name": "Dow Jones Industrial Average",
        "country": "Unites States",
        "components": sf.tickers_dow(),
        "suffix": "",
        "symbol": "^DJI"
    },
    "S&P500": {
        "name": "The Standard and Poor's 500",
        "country": "United States",
        "components": sf.tickers_sp500(),
        "suffix": "",
        "symbol": "^GSPC"
    },
    "NASDAQ": {
        "name": "NASDAQ Composite Index",
        "country": "United States",
        "components": sf.tickers_nasdaq(),
        "suffix": "",
        "symbol": "^IXIC"
    },
    # "FTSE100": {
    #     "name": "Financial Times Stock Exchange",
    #     "country": "United Kingdom",
    #     "components": sf.tickers_ftse100(),
    #     "suffix": ".L",
    #     "symbol": "^FTSE"
    # },
    # "FTSE250": {
    #     "name": "Financial Times Stock Exchange",
    #     "country": "United Kingdom",
    #     "components": sf.tickers_ftse250(),
    #     "suffix": ".L",
    #     "symbol": ""
    # },
    # "IBOVESPA": {
    #     "name": "The Bovespa Index",
    #     "country": "Brazil",
    #     "components": sf.tickers_ibovespa(),
    #     "suffix": ".SA",
    #     "symbol": "^BVSP"
    # },
    # "NIFTY50": {
    #     "name": "NIFTY 50 Index",
    #     "country": "India",
    #     "components": sf.tickers_nifty50(),
    #     "suffix": ".NS",
    #     "symbol": "^NSEI"
    # },
    # "NIFTYBANK": {
    #     "name": "NIFTY Bank Index",
    #     "country": "India",
    #     "components": sf.tickers_niftybank(),
    #     "suffix": ".NS",
    #     "symbol": "^NSEBANK"
    # },
}

ALPHA_NUM = {
    "0": "ZERO",
    "1": "ONE",
    "2": "TWO",
    "3": "THREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINE"
}

def get_table_name(index, symbol):
    # replace the special character at the start of index symbols with the word INDEX
    if symbol[0] == "^":
        return 'INDEX_' + index.replace('&', '_')
        
    table_name: str = symbol.replace('-', '_')
    table_name = table_name.replace('&', '_')
    table_name = table_name.replace(".", "_")
    table_name = table_name.replace("/", "_")

    if table_name[0].isdigit():
        table_name = table_name.replace(
            table_name[0], ALPHA_NUM[table_name[0]] + "_", 1)

    table_name = table_name + "_" + index.replace('&', '_')

    return table_name

def get_dataset_name(symbol, date: str, homogenous = True):
        
    table_name: str = symbol.replace('-', '_')
    table_name = table_name.replace('&', '_')
    table_name = table_name.replace(".", "_")
    table_name = table_name.replace("/", "_")

    if table_name[0].isdigit():
        table_name = table_name.replace(
            table_name[0], ALPHA_NUM[table_name[0]] + "_", 1)

    table_name = table_name + "_daily_dataset_" + date.replace("-", "")

    if not homogenous:
        table_name = "ref_" + table_name

    return table_name.lower()

def get_table_suffix(symbol):
        
    table_suffix: str = symbol.replace('-', '_')
    table_suffix = table_suffix.replace('&', '_')
    table_suffix = table_suffix.replace(".", "_")
    table_suffix = table_suffix.replace("/", "_")

    return table_suffix.lower()

# def remove_non_stocks(self, symbol: str, index):
#     # replace characters that are invalid in table names

#     nyse_stock_only = updated_nyse_to_array()
#     if symbol not in nyse_stock_only:
#         table_name = get_table_name(index, symbol)
#         self.stock_price_service.remove_table(table_name)
#     return

def show_index_lengths():
    print(("tickers_dow", len(sf.tickers_dow())))
    print(("tickers_ftse100", len(sf.tickers_ftse100())))
    print(("tickers_ftse250", len(sf.tickers_ftse250())))
    print(("tickers_ibovespa", len(sf.tickers_ibovespa())))
    print(("tickers_nasdaq", len(sf.tickers_nasdaq())))
    print(("tickers_nifty50", len(sf.tickers_nifty50())))
    print(("tickers_niftybank", len(sf.tickers_niftybank())))
    print(("tickers_other", len(sf.tickers_other())))
    print(("tickers_sp500", len(sf.tickers_sp500())))

holidays = ['2019-04-19', '2019-05-27', '2019-04-07', '2019-02-09',
            '2019-11-28', '2019-12-25', '2020-01-01', '2020-01-20',
            '2020-02-17', '2020-04-10', '2020-05-25', '2020-07-03',
            '2020-09-07', '2020-11-26', '2020-12-25', '2021-01-01',
            '2021-01-18','2021-02-15','2021-04-02','2021-05-31','2021-07-05',
            '2021-09-06','2021-11-25','2021-12-24','2022-01-17','2022-02-21',
            '2022-04-15','2022-05-30','2022-06-20','2022-07-04','2022-09-05',
            '2022-11-24','2022-12-26']

def get_last_busyday(date: str = datetime.date.today().isoformat()):
    target_date = datetime.date.fromisoformat(date)
    temp = np.busday_offset(target_date, 0, roll='backward', holidays=holidays)
    today = datetime.date.today()

    if temp == today:
        return np.busday_offset(today - datetime.timedelta(days=1), 0, roll='backward', holidays=holidays).astype(datetime.date)
    else:
        return temp.astype(datetime.date)

# initial client screening conditions
# "AND close > sma150 " +
# "AND close > sma200 " +
# "AND sma150 > sma200 " +
# "AND sma50 > sma150 " +
# "AND close > sma50 " +
# "AND close >= (1.3*low_52_week) " +
# "AND close >= (0.75*high_52_week) " +