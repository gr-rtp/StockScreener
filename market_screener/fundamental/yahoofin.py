import yahoo_fin.stock_info as si


def get_dow_list():
    return si.tickers_dow()