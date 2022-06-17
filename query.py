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
import apis.stock_output as so
import apis.stock_formula as sf
import apis.futu_api as fa
import apis.matplot as mp


ts.set_token('eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884')
token = 'eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884'
pro = ts.pro_api(token)

ts_code = '600833.SH'
start_date = 20220101
end_date = 20220608

stock = sa.bollinger_bands_strategy(ts_code=ts_code, start_date=start_date, end_date=end_date)
# stock.to_csv('stock/testing.csv', index=True, sep=',')
mp.plot_candle(stock, '000960.SZ')

# mp.plot_scatter(stock, 'volratio5','forcasting5','testing')

