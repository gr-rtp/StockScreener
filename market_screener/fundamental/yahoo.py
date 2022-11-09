import yfinance as yf
import pandas as pd

# This function returns the stock institutional holders info


def get_inst_info(symbol):
    ticker_object = yf.Ticker(symbol)
    df2 = ticker_object.institutional_holders
    if df2 is None:
        return list()

    try:
        holderlist = df2['Holder'].tolist()
    except KeyError:
        return list()
    sharelist = df2['Shares'].tolist()
    datelist = df2['Date Reported'].tolist()
    percentlist = df2['% Out'].tolist()
    valuelist = df2['Value'].tolist()

    List = list()
    for i in range(len(holderlist)):
        Dict = {
            'holder': holderlist[i],
            'share': sharelist[i],
            'datereported': datelist[i],
            'sharepercentage': percentlist[i],
            'value': valuelist[i]
        }
        List.append(Dict)

    return List

# This function returns the stock major holders info


def get_major_holders(symbol):
    ticker_object = yf.Ticker(symbol)
    df1 = ticker_object.major_holders
    if df1 is None:
        return dict()
    SharesValue_List = df1[0].tolist()
    Describelist = df1[1].tolist()

    Dict = {
        Describelist[0]: SharesValue_List[0],
        Describelist[1]: SharesValue_List[1],
        Describelist[2]: SharesValue_List[2],
        Describelist[3]: SharesValue_List[3]
    }
    return Dict

# This function returns the stock volume change info


def get_volume_change(symbol):
    ticker_object = yf.Ticker(symbol)
    df = ticker_object.history(period='6mo')
    vollist = df['Volume'].to_list()
    try:
        volch_10_up = 0
        volch_20_up = 0
        volch_50_up = 0
        volch_100_up = 0

        for i in range(0, 100):
            if i < 10 and vollist[-1 - i] - vollist[-2 - i] >= 0:
                volch_10_up = volch_10_up + 1
                volch_20_up = volch_20_up + 1
                volch_50_up = volch_50_up + 1
                volch_100_up = volch_100_up + 1

            if i >= 10 and i < 20 and vollist[-1 - i] - vollist[-2 - i] >= 0:
                volch_20_up = volch_20_up + 1
                volch_50_up = volch_50_up + 1
                volch_100_up = volch_100_up + 1
            if i >= 20 and i < 50 and vollist[-1 - i] - vollist[-2 - i] > 0:
                volch_50_up = volch_50_up + 1
                volch_100_up = volch_100_up + 1
            if i >= 50 and i < 100 and vollist[-1 - i] - vollist[-2 - i] > 0:
                volch_100_up = volch_100_up + 1

        volch_10_down = 10 - volch_10_up
        volch_20_down = 20 - volch_20_up
        volch_50_down = 50 - volch_50_up
        volch_100_down = 100 - volch_100_up

        up_div_down_10 = volch_10_up / volch_10_down
        up_div_down_20 = volch_20_up / volch_20_down
        up_div_down_50 = volch_50_up / volch_50_down
        up_div_down_100 = volch_100_up / volch_100_down

        Dict = {
            'VolumeUpDays(10d)': volch_10_up,
            'VolumeUpDays(20d)': volch_20_up,
            'VolumeUpDays(50d)': volch_50_up,
            'VolumeUpDays(100d)': volch_100_up,
            'VolumeDownDays(10d)': volch_10_down,
            'VolumeDownDays(20d)': volch_20_down,
            'VolumeDownDays(50d)': volch_50_down,
            'VolumeDownDays(100d)': volch_100_down,
            'Volumeup/downratio(10d)': up_div_down_10,
            'Volumeup/downratio(20d)': up_div_down_20,
            'Volumeup/downratio(50d)': up_div_down_50,
            'Volumeup/downratio(100d)': up_div_down_100,
        }
        return Dict

    except IndexError:
        Dict = {
            'VolumeUpDays(10d)': None,
            'VolumeUpDays(20d)': None,
            'VolumeUpDays(50d)': None,
            'VolumeUpDays(100d)': None,
            'VolumeDownDays(10d)': None,
            'VolumeDownDays(20d)': None,
            'VolumeDownDays(50d)': None,
            'VolumeDownDays(100d)': None,
            'Volumeup/downratio(10d)': None,
            'Volumeup/downratio(20d)': None,
            'Volumeup/downratio(50d)': None,
            'Volumeup/downratio(100d)': None
        }
        return Dict
