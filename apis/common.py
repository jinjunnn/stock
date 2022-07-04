import datetime
import os
import sys
import time
import json
import csv
import re
import random
from decimal import Decimal

#去掉股票后缀
def remove_suffix(stock_code):
    if stock_code[0] == '6':
        return stock_code[0:6]
    else:
        return stock_code[0:6]

# 将股票代码和股票交易所翻转, 如: 600000.SH -> SH.600000,用于富途API
def modify_stockcode(stock_code):
    if stock_code[0] == '6':
        return 'SH.' + stock_code[0:6]
    else:
        return 'SZ.' + stock_code[0:6]


# 添加股票后缀，用于查询tushare 代码
def add_stockcode_suffix(stock_code):
    if stock_code[0] == '6':
        return stock_code[0:6] + '.SH'
    else:
        return  stock_code[0:6] + '.SZ'


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
    x,y,z = zip(*l)
    return dict(zip(x,y))

#字符串类型的数据，用于查询富途数据
def date_shift(days):
    return (datetime.datetime.now()-datetime.timedelta(days=days)).strftime('%Y-%m-%d')

#字符串类型的数据，用于查询富途数据
def today():
    return datetime.datetime.now().strftime('%Y-%m-%d')

# 数字类型的日期，用于 yfinance 查询数据
def today_int():
    return int(datetime.datetime.now().strftime('%Y%m%d'))

# 数字类型的日期，用于 yfinance 查询数据
def today_int_shift(days):
    return int((datetime.datetime.now()-datetime.timedelta(days=days)).strftime('%Y%m%d'))

# 将列表转换为trading view可以上传的TXT文件
def convert_to_trading_view_file(stocklist):
    _list = []
    for item in stocklist:
        if item[0] == '6':
            _list.append('SSE:{}'.format(item))
        else :
            _list.append('SZSE:{}'.format(item))
        s = pd.DataFrame(_list)
        s['null'] = None
        s.to_csv('/Users/pharaon/Project/stock/stock/testing.txt', index=False, sep=',')
        