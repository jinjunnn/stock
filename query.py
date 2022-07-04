import tushare as ts
import pandas as pd
import numpy as np
import datetime
import os
import sys
import time
import json
import requests
import csv
import re
import random
import talib as ta
import pandas_ta as pa
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


import apis.stock_api as sa
import apis.futu_api as fa
import apis.matplot as mp


ts.set_token('eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884')
token = 'eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884'
pro = ts.pro_api(token)

ts_code = '600833.SH'
start_date = 20220101
end_date = 20220608

# stock = sa.bollinger_bands_strategy(ts_code=ts_code, start_date=start_date, end_date=end_date)
# stock.to_csv('stock/testing.csv', index=True, sep=',')
# mp.plot_candle(stock, '000960.SZ')

# mp.plot_scatter(stock, 'volratio5','forcasting5','testing')


reader = csv.reader(open('/Users/pharaon/Project/stock/file/top20.csv', 'r'))
stock_list = []
for item in reader:
    stock_list.append(item[0].replace("'",""))

_list = []
for item in stock_list:
    if item[0] == '6':
        _list.append('SSE:{}'.format(item))
    else :
        _list.append('SZSE:{}'.format(item))
print(_list)

s = pd.DataFrame(_list)
s['null'] = None
s.to_csv('stock/testing.csv', index=False, sep=',')

