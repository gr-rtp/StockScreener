import mongo
import yahoofin


# symbols = yahoofin.get_dow_list()
# symbols2 = list()
# for i in range(2, len(symbols)):
#     symbols2.append(symbols[i])
# symbols2.append('TSLA')
# symbols2.append('COIN')
# print(symbols2)
#
#
#
symbols2 = [ 'ORCL', 'SQ', 'ENPH', 'MELI', 'LMT', 'AMZN', 'V', 'FB', 'OTEX', 'EQIX',
            'SNOW',  'OTEX', 'BAM',  'AZO', 'CRWD', 'HYFM', 'ZS', ]
db = mongo.MGDB()
db.insert_multiple_symbols('showcase', 'data2', symbols2)

# my_file = open("D:/stockscreenergit/market_screener/sp500_daily_dataset.txt", "r")
# content_list = my_file.readlines()
#
# for i in range(len(content_list)):
#     content_list[i] = content_list[i].strip()
#
# print(content_list)
# db.insert_multiple_symbols('pass','data',content_list)

# 'AAPL', 'PANW', 'CHKP', 'ORLY', "RADA", 'TSLA', 'SQM', 'LMT', 'MSFT', 'FTNT',
#             'SFM', 'GOOGL', 'CTS',


