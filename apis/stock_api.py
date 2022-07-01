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

#设置tushare pro的token并获取连接
ts.set_token('eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884')
token = 'eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884'
pro = ts.pro_api(token)

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

#tushare 查询股票公司情况
def get_stock_company(code):
    df = pro.stock_basic(ts_code=code, fields='name,area,industry,is_hs')
    return df.iloc[-1]

#tushare获取股票数据
# ,ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount
def get_stock_data(ts_code,start_date,end_date):
    # print(ts_code,start_date,end_date)
    # df = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=str(start_date), end_date=str(end_date)) # 获得前复权日线数据
    return df.iloc[::-1] # 倒序

#查询指数信息
def get_index_daily(code,start_date,end_date):
    print(code,start_date,end_date)
    df = pro.index_daily(ts_code=code, start_date=start_date, end_date=end_date)
    return df.iloc[::-1] # 倒序

#查询基金信息
def get_fund_basic(ts_code,start_date,end_date):
    df = pro.index_daily(ts_code=ts_code,start_date=start_date, end_date=end_date)
    return df.iloc[::-1]

#获取指数列表
def get_index_list(market):
    df = pro.index_basic(market=market)
    df.to_csv('/Users/pharaon/Project/stock/file/index.csv', index=False, sep=',')
    return df

# cci_strategy 策略，返回数据表格
def cci_strategy(df,cci_timeperiod,cci_sum_timeperiod,cci_max_falling_rating_timeperiod):
    df['cci'] = ta.CCI(df['high'], df['low'], df['close'],timeperiod=cci_timeperiod)
    df['cci_shift'] = df['cci'].shift()
    df['cci_sum'] = df.apply(lambda x: sum_of_columns(df,x,cci_sum_timeperiod,'cci_shift'),axis=1) # 前5天cci之和 行数选择 4结果是5行。
    df['max_falling_rating'] = df.apply(lambda x:max_changing_rate(df, x, cci_max_falling_rating_timeperiod, 'close'), axis=1) # 前20天cci最大振幅
    df['SLOP'] = ta.LINEARREG_SLOPE((df['close'] + df['high'] + df['low'])/3, timeperiod=9)
    df['ANGLE'] = ta.LINEARREG_ANGLE((df['close'] + df['high'] + df['low'])/3, timeperiod=9)
    df['stoch'] = df.apply(lambda x:stoch(df, x, cci_max_falling_rating_timeperiod, 'close'), axis=1) # 前20天cci最大振幅
    df['ema'] = ta.EMA((df['close'] + df['high'] + df['low'])/3, 20) # 30天的指数移动平均
    df['ema_upper'] = df.apply(lambda X: X['ema'] + X['ema'] * 0.1, axis=1) # 30天的指数移动平均 升高10%
    df['ema_lower'] = df.apply(lambda X: X['ema'] - X['ema'] * 0.1, axis=1) # 30天的指数移动平均 降低10%
    df['envelope'] = df.apply(lambda x: 1 if (x['close'] > x['ema_upper']) else ( -1 if x['close'] < x['ema_lower'] else 0) , axis=1)
    df['envelope_shift'] = df['envelope'].shift()
    df['vol_shift'] = df['vol'].shift()
    df['vol_cal'] = df.apply(lambda x: sum_of_columns(df,x,5,'vol_shift') ,axis=1) # 
    
    # df['']
    df = df.fillna(value=1)
    df['quantityrelativeratio'] = df.apply(lambda x: x['vol'] * 5 / x['vol_cal'] if x['vol_cal'] != 0 else 1,axis=1)
    df['cci_status'] = df.apply(lambda x: 'buy' if (x['cci_sum']<-1000 and x['cci_shift'] <-100 and x['cci'] > -100 ) else 'wait' , axis=1)
    df['envelope_days'] = df.apply(lambda x: count_position(x['envelope'],x['envelope_shift']),axis=1) # envelope 在某一个状态持续的时间。
    # 删除cci列
    
    df1 = df.drop(['cci_shift','vol_shift','pre_close','change','amount','vol_cal'],axis=1)  # 去除无用列
    df2 = df1.round({'cci':1,'cci_sum':1,'max_falling_rating':2,'SLOP':2,'ANGLE':2,'stoch':2,'ema':1,'ema_upper':1,'ema_lower':1,'quantityrelativeratio':2}) # 保留这些字段一位小数
    return df2

def bollinger_bands_strategy(df):
    # ts_code,start_date,end_date 参数是这几个，这里做了调整，拆分了这个函数，直接传入DF
    bollinger_width_limit = 10
    timeperiod = 20
    multup = 2.0
    multdn =2.0

    # if end_date == None:
    #     end_date = time.strftime('%Y%m%d')

    # df = get_stock_data(ts_code,start_date,end_date)
    try:
        df['hlc3'] = pa.hlc3(df['high'], df['low'], df['close'])
        df['t_chg'] = (df['close'] - df['open']) / df['open'] * 100
        bbands = pa.bbands(df['hlc3'],length = timeperiod, std=2, mamode="ema", ddof = 0)

        df['ema_lower'] = bbands['BBL_20_2.0']
        df['ema'] = bbands['BBM_20_2.0']
        df['ema_upper'] = bbands['BBU_20_2.0']
        df['bandwidth'] = bbands['BBB_20_2.0']
        df['bandwidth_chg'] = df['bandwidth'] - bbands['BBB_20_2.0'].shift()
        df['percent'] = bbands['BBP_20_2.0']

        # df['ema'] = pa.ema(df['hlc3'],length=20)
        macd = pa.macd(df['hlc3'],fast=12,slow=26,signal=9)
        df['macd'] = macd['MACD_12_26_9']
        df['histogram'] = macd['MACDh_12_26_9']
        df['signal']=macd['MACDs_12_26_9']

        # 布林带宽度 与前几日均值的比，如果大于1 表明宽度在放大，小于1表明宽度在缩小。
        df['avgwidthratio30'] = df.apply(lambda x: volume_ratio(df,x,30,'bandwidth') ,axis=1)
        df['avgwidthratio20'] = df.apply(lambda x: volume_ratio(df,x,20,'bandwidth') ,axis=1)
        df['avgwidthratio10'] = df.apply(lambda x: volume_ratio(df,x,10,'bandwidth') ,axis=1)
        df['avgwidthratio5'] = df.apply(lambda x: volume_ratio(df,x,5,'bandwidth') ,axis=1)

        df['rsi'] = pa.rsi(df['hlc3'],length=13)
        df['cci'] = pa.cci(df['high'], df['low'], df['close'],length=13)

        # 量比 和 价格比 核实量价背离对否对指标有影响
        df['volratio5'] = df.apply(lambda x: volume_ratio(df,x,5,'vol') ,axis=1) # 
        df['volratio10'] = df.apply(lambda x: volume_ratio(df,x,10,'vol') ,axis=1) # 
        df['volratio3'] = df.apply(lambda x: volume_ratio(df,x,3,'vol') ,axis=1) # 
        df['pirceratio5'] = df.apply(lambda x: volume_ratio(df,x,5,'hlc3') ,axis=1) # 
        df['pirceratio10'] = df.apply(lambda x: volume_ratio(df,x,10,'hlc3') ,axis=1) # 
        df['priceratio3'] = df.apply(lambda x: volume_ratio(df,x,3,'hlc3') ,axis=1) # 

        # forcasting 预测之后涨跌状况
        df['forcasting1'] = df.apply(lambda x: forcasting(df,x,1,'t_chg'),axis=1)
        df['forcasting5'] = df.apply(lambda x: forcasting(df,x,5,'t_chg'),axis=1) # 

        # 斜率 和 平均值的比，如果大于1 表明斜率在放大，小于1表明斜率在缩小。
        df['lineangle10'] = ta.LINEARREG_ANGLE(df['hlc3'],timeperiod=10)
        df['lineangle20'] = ta.LINEARREG_ANGLE(df['hlc3'],timeperiod=20)
        df['lineangle30'] = ta.LINEARREG_ANGLE(df['hlc3'],timeperiod=30)
        # df['key'] = df['trade_date'] + df['ts_code']
        df = df.fillna(value=1)

        df1 = df.drop(['pre_close','change','amount',],axis=1)  # 去除无用列
        df2 = df1.round({
                        't_chg':3,
                        'lineangle10':3,
                        'lineangle20':3,
                        'lineangle30':3,
                        'bandwidth':3,
                        'bandwidth_chg':3,
                        'percent':3,
                        'ema_upper':3,
                        'ema':3,
                        'ema_lower':3,
                        'hlc3':3,
                        'macd':3,
                        'histogram':3,
                        'signal':3,
                        'avgwidthratio30':3,
                        'avgwidthratio20':3,
                        'avgwidthratio10':3,
                        'avgwidthratio5':3,
                        'rsi':3,
                        'cci':3,
                        'volratio5':3,
                        'volratio10':3,
                        'volratio3':3,
                        'pirceratio5':3,
                        'pirceratio10':3,
                        'priceratio3':3,
                        'forcasting1':3,
                        'forcasting5':3,
                        }) # 保留这些字段一位小数
        print(df2)
        return df2[20:]
    except  Exception as e:
        print(e)
        return None

def fund_bollinger_bands_strategy(ts_code,start_date,end_date):
    timeperiod = 20
    multup = 2.0
    multdn =2.0
    if end_date == None:
        end_date = time.strftime('%Y%m%d')
    df = get_fund_basic(ts_code,start_date,end_date)
    try:
        df['hlc3'] = pa.hlc3(df['high'], df['low'], df['close'])
        bbands = pa.bbands(df['hlc3'],length = timeperiod, std=2, mamode="ema", ddof = 0)
        df['ema_lower'] = bbands['BBL_20_2.0']
        df['ema'] = bbands['BBM_20_2.0']
        df['ema_upper'] = bbands['BBU_20_2.0']
        df['bandwidth'] = bbands['BBB_20_2.0']
        df['bandwidth_chg'] = df['bandwidth'] - bbands['BBB_20_2.0'].shift()
        df['percent'] = bbands['BBP_20_2.0']

        # df['key'] = df['trade_date'] + df['ts_code']
        df = df.fillna(value=1)
        return df[20:]
    except:
        return None

# 定义一个smma函数
def smma(price,sma,sma_shift,length):
    #创建一个pandas 函数
    if sma_shift==0:
        return sma
    else :
        return (sma_shift * ( length -1 ) + price )/length

# 定义一个鳄鱼线方法
def add_alligator(df):
    jaw = 13
    teeth = 8
    lips = 5
    try:
        # df['oc2'] = (df['open'] + df['close'])/2
        df['sma13'] = pa.sma(df['close'],length=jaw)
        df['sma8'] = pa.sma(df['close'],length=teeth)
        df['sma5'] = pa.sma(df['close'],length=lips)
        df['sma_shift13'] = pa.sma(df['close'],length=jaw).shift()
        df['sma_shift8'] = pa.sma(df['close'],length=teeth).shift()
        df['sma_shift5'] = pa.sma(df['close'],length=lips).shift()

        df['lips'] = df.apply(lambda x: smma(x['close'],x['sma5'],x['sma_shift5'],5) ,axis=1).shift(3)
        df['teeth'] = df.apply(lambda x: smma(x['close'],x['sma8'],x['sma_shift8'],8) ,axis=1).shift(5)
        df['jaw'] = df.apply(lambda x: smma(x['close'],x['sma13'],x['sma_shift13'],13) ,axis=1).shift(8)
        df['alligator_width'] = (df['lips'] - df['jaw'])/ df['close'] * 100
        df['alligator_width_chg'] = df['alligator_width'] - df['alligator_width'].shift()

        
        df['alligator_crossover'] = pa.cross(df['close'],df['teeth']) # 收盘价穿越 中线
        df = df.fillna(value=1)
        # df.to_csv('/Users/pharaon/Project/stock/file/test_alligator.csv', index=False, sep=',')
        return df
    except Exception as e:
        print('alligator error')
        print(e)

def add_vegas(df):
    try:
        df['ema144'] = pa.ema(df['close'],length=144)
        df['ema576'] = pa.ema(df['close'],length=576)
        df['ema169'] = pa.ema(df['close'],length=169)
        df['ema676'] = pa.ema(df['close'],length=676)
        df['vegas_crossover'] = pa.cross(df['close'],df['ema144'])  # 如果价格穿越 144天均线，值为1
        df = df.fillna(value=1)
        return df
    except Exception as e:
        print('alligator error')
        print(e)

