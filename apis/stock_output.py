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

import stock_formula as sf
import stock_api as sa


def output_stock_to_csv(stock):
    result = [stock.loc['ts_code'],stock.loc['trade_date'],stock.loc['close'],stock.loc['vol'],stock.loc['cci'],stock.loc['cci_shift'],stock.loc['cci_sum'],stock.loc['max_falling_rating'],stock.loc['stoch'],stock.loc['result']]
    return result


def write_csv(info,filename):
    with open(filename, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info)
        # 关闭文件
        csvfile.close()

