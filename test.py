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
import apis.ali_tablestore as alt
import apis.lean_cloud as lc

ts.set_token('eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884')
token = 'eb257271b6dd38501c139f0dcf7ddb949990c4384cae1f821c566884'
pro = ts.pro_api(token)

# print(1)

#生成一个空pandas dataframe
# df = pd.DataFrame()

#生成一个空pandas series

# for item in range(10):
#     s = pd.Series(data=[1,2,3,4,5],index=['ts_code', 'cci_12', 'cci_9', 'cci_20', 'date'])
#     df = df.append(s, ignore_index=True)

# _date=time.strftime('%Y%m%d')
# df.to_csv('/Users/jinjun/project/stock/stock/'+_date +'.csv', index=False, sep=',')


# l = [1,2,3,4,5]
# l.append(6)
# print(l)

# ts_code='600833.SH', start_date='2022-05-13 09:00:00', end_date='2022-05-13 13:45:00' ,freq='5min'

# def iter_stocks():
#     # 将股票信息写入 csv文件
#     stock_list = open('stock_list.csv', 'r')
#     reader = csv.reader(stock_list)
#     _date=time.strftime('%Y%m%d')
#     todaylist = pd.DataFrame()
#     for item in reader:
#         stock = sa.get_stock_min_exchange(item[1],start_date='2022-05-13 14:00:00', end_date='2022-05-13 14:50:00' ,freq='5min')
#         todaylist = todaylist.concat(stock, ignore_index=True)
#     todaylist.to_csv('/Users/jinjun/project/stock/stock/weipan'+_date +'.csv', index=False, sep=',')
#     # 将自选股发送到富途自选股app

# iter_stocks()


# 打开stock_list.csv文件
# stock_list = open('file/stock_list1.csv', 'r')
# reader = csv.reader(stock_list)

# dt = []
# for item in reader:
#     dt.append(item) if item[3][0:1] != '*' else None
# print(dt)

# 将股票信息写入 csv文件    
# stock_list = open('file/stock_list2.csv', 'w')
# writer = csv.writer(stock_list)
# writer.writerows(dt)


# 打开stock_list.csv文件

# 这个是将 trading view 中的股票信息写入 csv文件，



# df = pro.query('daily', ts_code='600833.SH', start_date=20220301, end_date=20220517)


# 查询某个股票信息
# start_date = 20220501
# end_date = 20220524
# df = pro.query('daily', ts_code='600833.SH', start_date=20220301, end_date=20220517)
# df = ts.pro_bar(ts_code='600833.SH', adj='qfq', start_date=str(start_date), end_date=str(end_date))
# df['result'] = pa.cross(df['close'], df['open'])
# pa.cross(df['close'], df['open'],asint=True)
# print(df)
# sa.get_stock_data('600833.SH', 20220301, 20220517)

# 线性回归斜率指标
# df = pd.DataFrame()
# s = pd.Series(data=[1,2,3,4,5,6,5,7,5,6])
# real2 = ta.LINEARREG(s, timeperiod=5)
# real = ta.LINEARREG_SLOPE(s, timeperiod=5)

# result = pd.concat([df,s])
# print(result)
# 将绩优股清单上传到富途商

# 从csv中导入 df
# df = pd.read_csv('stock/20220527bollingerband.csv', index_col=0)
# df.T.to_csv('stock/bollingerband1.csv', index=True, sep=',')


# s = pd.Series(data=[1,2,3,4,5,6,5,7,5,6])
# result = s.to_dict()
# print(result)
# print(type(result))


# 将df 的每一行 解析为 json
# df = pro.query('daily', ts_code='600833.SH', start_date=20220301, end_date=20220517)
# for index ,row in df.iterrows():
#     print(row.to_dict())


# 解析df 为 list of json
# df = pro.query('daily', ts_code='600833.SH', start_date=20220501, end_date=20220517)
# r = json.dumps(df.T.to_dict())
# print(r)
# for k, v in 
# #解析 json


# stock = sf.df_to_json(pro.query('daily', ts_code='000960.SZ', start_date=20220501, end_date=20220517))
# dynamodb.batch_writer_in_amazon_dynamodb('stock',stock)


# R = np.array([5,5,5,5,5,0])
# R_MEAN = np.mean(R)

# R_VAR = np.var(R)
# R_SC = np.mean((R-R_MEAN) ** 3)
# R_KU =  np.mean((R-R_MEAN) ** 4) / pow(R_VAR,2)

# print(R_SC)
# print(R_KU)



# print(help(pa.linreg))


# doc = sa.bollinger_bands_strategy(ts_code='002007.SZ', start_date=20000101, end_date=20220603)
# print(doc)
# doc.to_csv('stock/bollingerband2.csv', index=True, sep=',')


# 测试布林带策略，下载到csv
# stock = sa.bollinger_bands_strategy(ts_code='000960.SZ', start_date=20200101, end_date=20220608)
# stock.to_csv('stock/bollingerband2.csv', index=True, sep=',')


# pd.Series(data=[1,2,3,4,5,6,5,7,5,6,2,2,3,23,3,23,2,3,23,2,3,2,32,3,2,2])


# df = pro.query('daily', ts_code='600833.SH', start_date=20200501, end_date=20220517)
# print(df)
# fig, ax = plt.subplots()
# ax.plot(df['trade_date'], df['close'])
# ax.set_xlabel('Date')
# ax.set_ylabel('Price')
# ax.set_title('Price History')
# plt.show()


# 测试布林带策略，下载到csv
ts_code = '000960.SZ'
start_date = 20220101
end_date = 20220617


stock = sa.bollinger_bands_strategy(ts_code=ts_code, start_date=start_date, end_date=end_date)
# 保存到csv文件
# stock.to_csv('stock/001.csv', index=True, sep=',')
mp.plot_scatter(stock, 'volratio5','forcasting5','testing')



# stock.to_records('stock/test.json',orient='records')

# primary_key = [['key','imkey1'], ['trade_date','trade_date1'], ['ts_code','ts_code']]
# attribute_columns = [['name','John'], ['mobile',123], ['address','China'], ['age',123]]
# # # primary_key ={'key':'imkey', 'trade_date':'trade_date', 'ts_code':'ts_code'}
# # attribute_columns = {'name':'John', 'mobile':123, 'address':'China', 'age':123}

# alitb.put_row('trading',primary_key,attribute_columns)


# def bollinger_bands_strategy(ts_code,start_date,end_date):
#     df = sa.get_stock_data(ts_code,start_date,end_date)
#     # 布林带宽度 与前几日均值的比，如果大于1 表明宽度在放大，小于1表明宽度在缩小。
#     df['avgwidthratio30'] = df.apply(lambda x: sf.volume_ratio(df,x,5,'vol') ,axis=1)

# bollinger_bands_strategy(ts_code,start_date,end_date)


# df = pro.fund_basic(market='E')
# # 保存csv文件
# df.to_csv('stock/fund_basic.csv', index=True, sep=',')

# pre = [('code':)]
# arg = 


# sa.put_row('stock',)



# 删除tablestore 行数据
stock_list = open('file/total.csv', 'r')
reader = csv.reader(stock_list)
for item in reader:
    print(item)
    # print(sf.remove_suffix(item[1]))
    # try:
    #     response = alt.put_row('stock',[('code',sf.remove_suffix(item[1]))],[('askSize',0)])
    #     print(response)
    # except Exception as e:
    #     print(e)

