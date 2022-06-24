import csv
import json
import pandas as pd
import time
import datetime
import pandas_ta as pa
from tablestore import *


import apis.futu_api as ft
import apis.matplot as mp
import apis.stock_formula as sf

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

def futu_bollinger_bands_strategy(df):
    timeperiod = 20
    multup = 2.0
    multdn =2.0

    try:
        df['hlc3'] = pa.hlc3(df['high'], df['low'], df['close'])
        bbands = pa.bbands(df['hlc3'],length = timeperiod, std=2, mamode="ema", ddof = 0)
        df['ema_lower'] = bbands['BBL_20_2.0']
        df['ema'] = bbands['BBM_20_2.0']
        df['ema_upper'] = bbands['BBU_20_2.0']
        df['bandwidth'] = bbands['BBB_20_2.0']
        df['bandwidth_chg'] = df['bandwidth'] - bbands['BBB_20_2.0'].shift()
        df['percent'] = bbands['BBP_20_2.0']
        df['spike'] = df['close'] - df['open']
        df['spike_upper'] = pa.stdev(df['spike'], length = 100, ddof = 0)
        df['spike_lower'] = -pa.stdev(df['spike'], length = 100, ddof = 0)

        # df['ema'] = pa.ema(df['hlc3'],length=20)
        macd = pa.macd(df['hlc3'],fast=12,slow=26,signal=9)
        df['macd'] = macd['MACD_12_26_9']
        df['histogram'] = macd['MACDh_12_26_9']
        df['signal']=macd['MACDs_12_26_9']

        df = df.fillna(value=0)
        return df[20:]
    except Exception as e:
        print(e)
        print(12314)
        return None


#创建主函数
def main():
    # 获取股票代码
    code_row = input('input code = ')
    timelength = str(input('how many minite = '))
    # code_row = '600477'
    # timelength = '15'

    code = modify_stockcode(str(code_row))
    try :
        df = ft.get_history_kline(code, 'K_{}M'.format(timelength), date_shift(int(30)), today())
        try :
            stock = futu_bollinger_bands_strategy(df)
            #打印df最后一行
            primary_key =[('code',code_row)]
            attribute_columns = ['expectedIncrease','recommendationKey','averageAmplitude','beta','recommendationMean','targetMeanPrice']
            try :
                stock_row = get_row('stock',primary_key,attribute_columns)
                stockinfo = sf.tuple_to_dict(stock_row.attribute_columns)
                print(pd.DataFrame.from_dict(stockinfo, orient='index'))
            except Exception as e:
                print(e)
            print(stock.iloc[-1])
            mp.plot_boolinger(stock,code)
        except Exception as e:
            print(e)
            print('执行布林带策略出错')
    except:
        print('error')
        pass



#执行主函数
if __name__ == '__main__':
    main()
    # pass
