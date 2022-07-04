import csv
import json
import pandas as pd
import time
import datetime
import pandas_ta as pa
from tablestore import *

import sys
sys.path.append("./apis")
import futu_api as ft
import matplot as mp
import common

client = OTSClient("https://pharaontrade.cn-hangzhou.ots.aliyuncs.com", 'LTAI5tLWK2gTt8JB3kHkxyCa', 'xzlgVf6tbFBm3yNpUL54GnhdAi6oML', 'pharaontrade')

def date_shift(days):
    return ((datetime.datetime.now()-datetime.timedelta(days=days))).strftime('%Y-%m-%d')

def today():
    return datetime.datetime.now().strftime('%Y-%m-%d')

# 将股票代码和股票交易所翻转, 如: 600000.SH -> SH.600000
def modify_stockcode(stock_code):
    if stock_code[0] == '6':
        return 'SH.' + stock_code[0:6]
    else:
        return 'SZ.' + stock_code[0:6]

# def lowest(df, n):
#     return df.rolling(n).min()

# def highest(df, n):
#     return df.rolling(n).max()
def get_row(table_name,primary_key,columns_to_get):
    consumed, return_row, next_token = client.get_row(table_name, primary_key, columns_to_get)
    # print ('Read succeed, consume %s read cu.' % consumed.read)
    # print ('Value of primary key: %s' % return_row.primary_key)
    # print ('Value of attribute: %s' % return_row.attribute_columns)
    return(return_row)

#创建主函数
def doit():
    # 获取股票代码
    code_row = input('input code = ')
    timelength = str(input('how many minite = '))
    # code_row = '600477'
    # timelength = '15'

    code = modify_stockcode(str(code_row))
    try :
        df = ft.get_history_kline(code, 'K_{}M'.format(timelength), date_shift(int(30)), today())
        try :
            stock = ft.add_bollinger(df)
            #打印df最后一行
            primary_key =[('code',code_row)]
            attribute_columns = ['expectedIncrease','recommendationKey','averageAmplitude','beta','recommendationMean','targetMeanPrice']
            try :
                stock_row = get_row('stock',primary_key,attribute_columns)
                stockinfo = common.tuple_to_dict(stock_row.attribute_columns)
                print(pd.DataFrame.from_dict(stockinfo, orient='index'))
            except Exception as e:
                print(e)
            print(stock.iloc[-1])
            stock.to_csv('stock/12344.csv', index=False, sep=',')
            image_url = '/Users/pharaon/Downloads/stock/{}.png'.format(str(time.time()))
            last_kline = stock.iloc[-1]
            print(stock)
            mp.plot_boolinger(stock,code,image_url,last_kline)
            doit()
        except Exception as e:
            print(e)
            print('执行布林带策略出错')
            doit()
    except Exception as e:
        print(e)
        doit()


def main():
    doit()
#执行主函数
if __name__ == '__main__':
    main()
    # pass
