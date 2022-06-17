import csv
import yfinance as yf
import json
import pandas as pd
import time

# 从apis 文件夹中导入文件
import sys
sys.path.append("./apis")
import stock_api as sa
import stock_formula as sf
import yhshare as yh
import ali_tablestore as ats

def iter_stocks(source_path):
    #打开csv文件
    # stock_list = open('file/stock_list.csv', 'r')
    # reader = csv.reader(stock_list)
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)


    for item in reader:
        print(item)
        try:
            stock = ats.get_row('stock',[('code',sf.remove_suffix(item[1]))],['totalCash'])
            print(stock)
            print(stock.primary_key,stock.attribute_columns)
        except  Exception as e:
            print(e)



        # try:
        #     stock = get_stock_infomations(item[1])
        # except  Exception as e:
        #     print(e)

        # try:
        #     response = alt.put_row('stock',[('code',sf.remove_suffix(item[1]))],[('askSize',0)])
        #     print(response)
        # except Exception as e:
        #     print(e)

# iter_stocks('/Users/pharaon/Project/stock/file/total.csv')


# stock = ats.get_row('stock',[('code','000416')],['totalCash'])
# print(stock)

tickers = yf.Tickers('msft aapl goog')

print(tickers)