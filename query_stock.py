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

import stock_api as sa
import stock_output as so
import futu_api as fa
import tg
import ali_tablestore as ats


def iter_cci_strategy(resource_path):
    # 将股票信息写入 csv文件
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    _date=time.strftime('%Y%m%d')
    todaylist = pd.DataFrame()
    futu_faver = []
    for item in reader:
        stock = cci_strategy(item[1],0.15,20220301,None)
        print(stock)
        # 富途自选股 API 将符合规则的股票加入到自选股
        futu_faver.append(0) if stock['cci_status']=='buy' else None
        tg.send_word('2013737722','cci_strategy:\n' + stock.to_string()) if stock['cci_status']=='buy' else None
        todaylist = todaylist.append(stock, ignore_index=True)
    #将df保存为csv文件
    todaylist.to_csv('stock/'+_date +'.csv', index=False, sep=',')
    # 将自选股发送到富途自选股app
    fa.modify_favor('入选',futu_faver)
    
def cci_strategy(ts_code,time_interval,start_date,end_date):
    time.sleep(time_interval)
    start_date= start_date
    if end_date == None:
        end_date = time.strftime('%Y%m%d')
    df = sa.cci_strategy(sa.get_stock_data(ts_code,start_date,end_date),12,9,20) # 12日CCI指标
    return df.iloc[-1]


# iter_cci_strategy('file/faver_stock.csv')
# iter_cci_strategy('file/stock_list.csv')

def iter_get_up_candles(resource_path):
    # 将股票信息写入 csv文件
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    _date=time.strftime('%Y%m%d')

    for item in reader:
        stock = sa.get_up_candles(sa.get_stock_data(item[1],20180101,_date))
        print(stock)
        #将df保存为csv文件
        stock.to_csv('other/'+item[1] +'.csv', index=False, sep=',')

# iter_get_up_candles('file/faver_stock.csv')





def iter_bollinger_bands_strategy(resource_path):
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    _date=time.strftime('%Y%m%d')
    todaylist = pd.DataFrame()
    futu_faver = []
    i = 0
    for item in reader:
        time.sleep(0.1)
        df = sa.bollinger_bands_strategy(item[1],20220301,_date)
        # print(stock.iloc[-1])
        # print(stock.iloc[-2])
        longCondition = 'crossOverSMA' if df.iloc[-2].loc['hlc3'] < df.iloc[-2].loc['middleband'] and df.iloc[-1].loc['hlc3'] > df.iloc[-1].loc['middleband'] else ('crossOverLowerBand' if df.iloc[-2].loc['hlc3'] < df.iloc[-2].loc['lowerband'] and df.iloc[-2].loc['hlc3'] > df.iloc[-2].loc['lowerband'] else 'other')
        stock = df.iloc[-1]
        stock['condition'] = longCondition
        stock['url'] = 'https://gu.qq.com/sh600548/gp'
        todaylist[i] = stock
        i = i + 1
        print(todaylist.T)
        tg.send_word('2013737722','bollinger_bands_strategy:\n' + stock.to_string()) if longCondition !='other' else None
    todaylist.T.to_csv('stock/'+_date +'bollingerband.csv', index=False, sep=',')
# iter_bollinger_bands_strategy('file/faver_stock.csv')


# 将每日的股票数据上传到阿里云
def upload_stock_data_to_tablestore(resource_path,start_date,end_date):
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    _date=time.strftime('%Y%m%d')
    _list = pd.DataFrame()
    for item in reader:
        print(item)
        df = sa.bollinger_bands_strategy(ts_code=item[1], start_date=start_date, end_date=end_date)
        try:
            stock = df.tail(2)
            _list = _list.append(stock, ignore_index=True)
        except:
            pass
    ats.prepare_batch_write_data(_list)
        # mp.plot_scatter(stock, 'volratio5','forcasting5','testing')
        # stock.to_json('stock/' + item[1] + '.json',orient='records')


upload_stock_data_to_tablestore('file/total.csv',20220301,None)


# 讲符合规则的股票数据保存起来
def save_stock(resource_path,start_date,end_date):
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    _date=time.strftime('%Y%m%d')
    _list = pd.DataFrame()
    for item in reader:
        print(item)
        stock = sa.bollinger_bands_strategy(ts_code=item[1], start_date=start_date, end_date=end_date)
        # stock.to_csv('stock/' + item[1] + '.csv', index=False, sep=',')
        try:
            for index, row in stock.iterrows():
                if row['pct_chg'] >= 5.0 and row['10_chg_gt7'] == False:
                    _list = _list.append(row, ignore_index=True)
        except:
            pass
    _list.to_csv('stock/chg_gt7.csv', index=False, sep=',')
        # mp.plot_scatter(stock, 'volratio5','forcasting5','testing')
        # stock.to_json('stock/' + item[1] + '.json',orient='records')
# save_stock('file/faver.csv',20160101,20220612)

