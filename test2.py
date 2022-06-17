#  当用户输入股票名称和时间时，查询数据库，获取数据，并计算出各种指标
import talib as ta
import pandas as pd
import tushare as ts
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
import pandas_ta as pa



ts.set_token('eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884')
token = 'eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884'
pro = ts.pro_api(token)
aroon_imeperiod = 20    #阿隆周期参数
cci_imeperiod = 12  #CCI周期参数
count = 0   #统计阿龙指标在一个区间持续的天数
up_index = 70   # 阿龙指标 up值
down_index = 40 # 阿龙指标 down值



def aroon_position(up,down):
    if up > up_index and down < down_index:
        return 1
    elif up < down_index and up_index < down:
        return -1
    else:
        return 0

#统计阿龙指标在某一个周期持续的时间
def count_position(today,lastday):
    if today == lastday:
        global count
        count = count + 1
        return count
    else:
        result = count + 1
        count = 0
        return result

#计算 X 位置
def cal_x_position(today):
    if today > 100:
        return 1
    elif today > -100 and today < 100:
        return 0
    else:
        return -1
    

#计算 Y 位置
def cal_y_position(today,lastday):
    if today > lastday :
        return 1
    elif today < lastday:
        return -1
    else:
        return 0


#   顺势指标策略
def cal_z_status(today,lastday):
    if today == lastday:
        return 0
    if (today == 1 and lastday == 0) or  (today == 1 and lastday == -1)  or (today == 0 and lastday == -1):
        return 1
    elif  (today == 0 and lastday == 1) or  (today == -1 and lastday == 0)  or (today == -1 and lastday == 1):
        return -1
    else:
        return 100

def data_calculation(dframe):
    df=dframe
    _open = df['open']
    ts_code = df['ts_code']
    trade_date = df['trade_date']
    high = df['high']
    low = df['low']
    close = df['close']
    pre_close = df['pre_close']
    change = df['change']
    pct_chg = df['pct_chg']
    volume = df['vol']
    amount = df['amount']

    df['aroon_down'], df['aroon_up'] = ta.AROON(high, low, timeperiod=aroon_imeperiod)  
    df['aroon_down'] = df['aroon_down'].fillna(0)
    df['aroon_up'] = df['aroon_up'].fillna(0)
    df['index'] = df['aroon_up'] - df['aroon_down']

    df['aroon_position'] = df.apply(lambda x: aroon_position(x['aroon_up'],x['aroon_down']),axis=1) #阿隆指标是否符合策略 1：符合策略，-1：不符合策略，0：不符合策略
    df['aroon_position_lastday'] = df['aroon_position'].shift(1) # 前一天周期的结果
    df['aloon_position_account'] = df.apply(lambda x: count_position(x['aroon_position'],x['aroon_position_lastday']),axis=1)  # 统计阿龙指标在某一个周期持续的时间

    df['CCI'] = ta.CCI(high, low, close, timeperiod=cci_imeperiod) 
    df['CCI'] = df['CCI'].fillna(0)

    df['CCI_lastday'] = df['CCI'].shift(0) # 前一天周期的结果
    df['CCI_position'] = df.apply(lambda x: cal_x_position(x['CCI']),axis=1) # 顺势指标策略
    df['CCI_position_lastday'] = df['CCI_position'].shift(1) # 前一天周期的结果

    df['CCI_up_and_down'] = df.apply(lambda x: cal_y_position(x['CCI'],x['CCI_lastday']),axis=1) # 前一天周期的结果
    df['CCI_status'] = df.apply(lambda x: cal_z_status(x['CCI'],x['CCI_lastday']),axis=1) # 前一天周期的结果
    df.to_csv('data.csv', index=False)
    return df

def output_data(df,trade_date):
    row_index = df[df['trade_date']==trade_date].index.tolist() # 获取交易日的索引值
    print(df.iloc[row_index[0]])
    CCI_list = df.loc[row_index[0] + 5:row_index[0], 'CCI'] # 选取日前7天的CCI

    #获得pandas某一行的值
    print('CCI_list:',CCI_list)
    print('标准差 = ',CCI_list.std())
    print('均值 = ',CCI_list.mean())
    print('标准差/均值 = ',CCI_list.std()/CCI_list.mean())


def get_stock_data_by_name(share, trade_date):

    df = pro.query('daily', ts_code=share, start_date=20090101, end_date=time.strftime('%Y%m%d'))
    df = data_calculation(df.iloc[::-1])
    df = output_data(df,trade_date)


# s = pd.Series([1,2,3,4,5])
# print(s.std(),s.mean(),s.std()/s.mean())

# s1 = pd.Series([100,114,106,88,110])
# print(s1.std(),s1.mean(),s1.std()/s1.mean())

# get_stock_data_by_name('001202.Sz', '20220420')

# SHHAHA 