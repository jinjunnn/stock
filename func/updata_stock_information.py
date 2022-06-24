import csv
import yfinance as yf
import json
import pandas as pd
import time

# 从apis 文件夹中导入文件
import sys
sys.path.append("./apis")
import stock_api as sa
import common
import yhshare as yh
import ali_tablestore as ats
import tg
import futu_api as fa

def prepare_data(code,stock):
    for key in list(stock.keys()):
        if stock[key] == None:
            stock.pop(key)
    # 去掉这个值是列表的字段
    stock['companyOfficers'] = ''
    stock.pop('companyOfficers')

    primary_key = [['code', common.remove_suffix(code)]]
    attribute_columns = list(zip(tuple(stock), stock.values()))
    ats.update_row('stock',primary_key,attribute_columns)


def iter_stocks(source_path):
    print(1)
    #打开csv文件
    # stock_list = open('file/stock_list.csv', 'r')
    # reader = csv.reader(stock_list)
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)
    _list = []
    for item in reader:
        _list.append(item[1])
    n = 10
    print(_list)
    for i in range(0, len(_list), n):
        stocks = ' '.join(_list[i:i+n])
        print(stocks)
        # tickers = yf.Tickers('000877.SZ 002064.SZ')
        tickers = yf.Tickers(stocks)
        for ticker in tickers.tickers:
            print(ticker)
            try:
                prepare_data(ticker,tickers.tickers[ticker].info)
            except  Exception as e:
                print(e)
                tg.send_word(2013737722,'换服务器啦')
                time.sleep(15)
                try:
                    prepare_data(ticker,tickers.tickers[ticker].info)
                except Exception as e:
                    print(e)

# iter_stocks('/Users/pharaon/Project/stock/file/total.csv')

# 遍历一次云端历史数据，如果云端没有，则上传到云端
def iter_stocks_history(source_path):
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)
    for item in reader:
        code = common.yahoo_stockcode(item[2])
        stockinfo = ats.get_row('stock',[('code',item[2])],['country'])
        print(stockinfo)
        if stockinfo == None:
            try:
                stock = yf.Ticker(code)
                prepare_data(code,stock.info)
            except Exception as e:
                print(e)
                tg.send_word(2013737722,'换服务器啦')
                time.sleep(15)
                try:
                    stock = yf.Ticker(code)
                    prepare_data(code,stock.info)
                except Exception as e:
                    print(e)


# 更新股票的平均振幅
def uploadAverageAmplitude(source_path):
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)
    for item in reader:
        try:
            start_date = 20200101
            end_date = 20220620

            df = sa.get_stock_data(item[1], start_date, end_date)
            a = ((df['high'] - df['low']) / df['low']).mean() * 100
            # 保留两位小数
            a = round(a, 2)
            primary_key = [['code', common.remove_suffix(item[2])]]
            attribute_columns = [('averageAmplitude', a)]
            print(primary_key, attribute_columns)
            ats.update_row('stock',primary_key,attribute_columns)
        except Exception as e:
            print(e)
            # tg.send_word(2013737722,'换服务器啦')
            # time.sleep(15)
            # try:
            #     stock = yf.Ticker(code)
            #     prepare_data(code,stock.info)
            # except Exception as e:
            #     print(e)


# 更新距离目标价涨幅
def uploadTargetPrice(source_path):
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)
    for item in reader:
        try:
            close_row = sa.get_stock_data(item[1], common.today_int_shift(1), common.today_int_shift(1))
            close = close_row['close'].values[0]
            print('close:', close)
            targetMeanPrice_row = ats.get_row('stock',[('code',item[2])],['targetMeanPrice'])
            if targetMeanPrice_row != None:
                targetMeanPrice = targetMeanPrice_row.attribute_columns[0][1]
                print(targetMeanPrice_row.attribute_columns)
                print('targetMeanPrice:',targetMeanPrice)
                expectedIncrease = round((targetMeanPrice - close) / close * 100,2)
                print(expectedIncrease)
                primary_key = [('code',item[2])]
                attribute_columns = [('expectedIncrease', expectedIncrease)]
                print(primary_key, attribute_columns)
                print(item[2])
                ats.update_row('stock',primary_key,attribute_columns)
                print('...............')

                # time.sleep(10)
                # df = sa.get_stock_data(item[1], start_date, end_date)
                # a = ((df['high'] - df['low']) / df['low']).mean() * 100
                # # 保留两位小数
                # a = round(a, 2)
                # primary_key = [['code', common.remove_suffix(item[2])]]
                # attribute_columns = [('averageAmplitude', a)]
                # print(primary_key, attribute_columns)
                # ats.update_row('stock',primary_key,attribute_columns)
        except Exception as e:
            # print(targetMeanPrice)
            print(e)



# 设置条件，将符合条件的股票上传到富途证券APP
def uploadStrongBuyToFutu(source_path):
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)
    _list = []
    for item in reader:
        try:
            stockinfo = ats.get_row('stock',[('code',item[2])],['expectedIncrease','recommendationKey','symbol','averageAmplitude'])
            stock = common.tuple_to_dict(stockinfo.attribute_columns)
            
            try :
                CONDITION = stock['expectedIncrease'] > 70 and (stock['recommendationKey'] == 'strong_buy' or stock
                ['recommendationKey'] == 'buy') and stock['averageAmplitude'] > 4
                LABLE = 'first'
                if CONDITION:
                    print(common.modify_stockcode(item[2]))
                    _list.append(common.modify_stockcode(item[2]))
                    if len(_list) == 20:
                        print(_list)
                        fa.modify_favor(LABLE,_list)
                        _list = []
                # if stockinfo.attribute_columns[0][1] > 30 and stockinfo.attribute_columns[1][1] == 'strong_buy':
                #     print(common.modify_stockcode(item[2]))
                # _list.append(modify_stockcode(item[2]))
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    fa.modify_favor(LABLE,_list)


# uploadStrongBuy('/Users/pharaon/Project/stock/file/total.csv')

# stock = ats.get_row('stock',[('code','000416')],['country'])
# print(common.tuple_to_dict(stock.attribute_columns))