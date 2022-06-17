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
from decimal import Decimal

# 计算一个区间的总额
def sum_of_columns(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name, _key]
        return result.sum()
    except:
        pass

# 计算一个区间的均值
def avg_of_columns(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name, _key]
        return result.sum() / timeperiod
    except:
        pass

# 计算量比
def volume_ratio(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name + 1, _key]
        return stock.loc[row.name,_key] / result.mean()
    except:
        pass

# 查看某个字段未来几日的涨跌幅度
def forcasting(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name -1:row.name - timeperiod, _key]
        return result.sum()
    except:
        pass


def max_of_columns(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name + 1, _key]
        return result.max()
    except:
        pass

def min_of_columns(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name + 1, _key]
        return result.min()
    except:
        pass

# 从最高值下降了的百分比
def falling_rate(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name, _key]
        _max = result.max()
        _current = row.loc[_key]
        return (_current - _max) / _max
    except:
        pass

# 从最低值上升了的百分比
def rising_rate(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name, _key]
        _min = result.min()
        _current = row.loc[_key]
        return (_current - _min) / _min
    except:
        pass

# 最高点到最低点的变化百分比
def max_changing_rate(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name, _key]
        _max = result.max()
        _min = result.min()
        return (_max - _min) / _max
    except:
        pass

# 当前值在最高值和最低值的区间 的百分比
def stoch(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name + timeperiod:row.name, _key]
        _max = result.max()
        _min = result.min()
        _current = row.loc[_key]
        result = (_current - _min) / (_max - _min) if (_max - _min) != 0 else 0
        return result
    except:
        pass

#去掉股票后缀
def remove_suffix(stock_code):
    if stock_code[0] == '6':
        return stock_code[0:6]
    else:
        return stock_code[0:6]

# 将股票代码和股票交易所翻转, 如: 600000.SH -> SH.600000
def modify_stockcode(stock_code):
    if stock_code[0] == '6':
        return 'SH.' + stock_code[0:6]
    else:
        return 'SZ.' + stock_code[0:6]

# 计算持续一个状态的日期综合
count = 0
def count_position(today,lastday):
    global count
    if today == lastday:
        count = count + 1
        return count
    else:
        count = 0
        return count


# 将下载的trading view 股票数据转换为 csv文件。  
def set_faver_to_futu_from_tradingview(from_path,to_path):
    stock_list = open(from_path, 'r')
    reader = csv.reader(stock_list)
    result = []
    result2 = []
    for item in reader:
        for i in item:
            if i[0:2] == 'SS':
                s = i[-6:]+'.SH'
                ix = i[-6:]
                f = 'SH.{}'.format(ix)
                result2.append(f)
                result.append([0,s])
            else:
                s = i[-6:]+'.SZ'
                ix = i[-6:]
                f = 'SZ.{}'.format(ix)
                result2.append(f)
                result.append([0,s])
    stock_list1 = open(to_path, 'w')
    writer = csv.writer(stock_list1)
    writer.writerows(result)


# set_faver_to_futu_from_tradingview('file/faver.csv','file/faver_stock.csv')

# 将 df 解析为 dict 的list
def df_to_json(df):
    # 这个是对 每一行解析
    l = []
    for index ,row in df.iterrows():
        item = row.to_dict()
        l.append(json.loads(json.dumps(item), parse_float=Decimal))
    return l

# 字典解析为元组
def dict_to_tuple(d):
    return list(zip(tuple(d),tuple(d.values())))

# 元组解析为字典
def tuple_to_dict(l):
    k,v = zip(*l)
    return dict(zip(k,v))
