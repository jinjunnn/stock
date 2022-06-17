# 通过雅虎财经获取历史数据
import yfinance as yf
import json
import csv
import pandas as pd
import time

import lean_cloud as lc
import ali_tablestore as ats
import stock_output as so
import stock_formula as sf


def get_stock_bars(stock):
    data = yf.download(stock, period="max")
    return data

# msft = yf.Ticker("000960.SZ")


def get_stock_infomations(code):
    try:
        stock = yf.Ticker(code)
        for key in list(stock.keys()):
            if stock[key] == None:
                stock.pop(key)
        # 去掉这个值是列表的字段
        stock['companyOfficers'] = ''
        stock.pop('companyOfficers')
        return stock
    except:
        pass


# 获取股票清单中股票的预期收益等信息。
def iter_stock_infomations(resource_path):
    _list = open(resource_path, 'r')
    reader = csv.reader(_list)
    todaylist = pd.DataFrame()
    futu_faver = []
    i = 0
    for im in reader:
        time.sleep(1)
        try:
            msft = yf.Ticker(im[1])
            stock = msft.info
            # stock.pop('longBusinessSummary')
            # stock.pop('website')
            # stock.pop('address2')
            # stock.pop('address1')
            # stock.pop('fullTimeEmployees')
            # stock.pop('exchange')
            # stock.pop('country')
            # stock.pop('exchangeTimezoneName')
            # stock.pop('exchangeTimezoneShortName')
            # stock.pop('messageBoardId')
            # stock.pop('market')
            # stock.pop('logo_url')
            # stock.pop('phone')
            # stock.pop('financialCurrency')
            # stock.pop('zip')
            # stock.pop('city')
            # stock.pop('fax')
            # stock.pop('shortName')
            # stock.pop('longName')
            for key in list(stock.keys()):
                if stock[key] == None:
                    stock.pop(key)

            primary_key = [['code', sf.remove_suffix(im[1])]]
            attribute_columns = list(zip(tuple(stock), stock.values()))
            print(primary_key)
            ats.put_row('stock',primary_key,attribute_columns)

            # print(msft.info['trailingEps'])
            # print(msft.info['targetMeanPrice'])
            # print(msft.info['targetLowPrice'])
            # print(msft.info['targetMedianPrice'])
            # print(msft.info['targetHighPrice'])
            # item = [im[1]]
            # print(type(item),item)
            # item.append(msft.info['trailingEps'])
            # item.append(msft.info['targetLowPrice'])
            # item.append(msft.info['targetMeanPrice'])
            # item.append(msft.info['targetMedianPrice'])
            # item.append(msft.info['targetHighPrice'])
            # print(item)
            # todaylist[i] = item
            # i = i + 1
            # print(todaylist.T)

        # except Exception as e:
        #     print(e)
        #     print(im[1])
        #     try:
        #         time.sleep(61)
        #         msft = yf.Ticker(im[1])
        #         stock = msft.info
        #         # stock.pop('companyOfficers')
        #         # stock.pop('longBusinessSummary')
        #         # stock.pop('website')
        #         # stock.pop('address2')
        #         # stock.pop('address1')
        #         # stock.pop('fullTimeEmployees')
        #         # stock.pop('exchange')
        #         # stock.pop('country')
        #         # stock.pop('exchangeTimezoneName')
        #         # stock.pop('exchangeTimezoneShortName')
        #         # stock.pop('messageBoardId')
        #         # stock.pop('market')
        #         # stock.pop('logo_url')
        #         # stock.pop('phone')
        #         # stock.pop('financialCurrency')
        #         # stock.pop('zip')
        #         # stock.pop('city')
        #         # stock.pop('fax')
        #         # stock.pop('shortName')
        #         # stock.pop('longName')
        #         for key in list(stock.keys()):
        #             if stock[key] == None:
        #                 stock.pop(key)
        #         primary_key = [['code', sf.remove_suffix(im[1])]]
        #         attribute_columns = list(zip(tuple(stock), stock.values()))
        #         print(attribute_columns)
        #         ats.put_row('stock',primary_key,attribute_columns)
        except Exception as e:
            print(e)
            print(im[1])
            so.write_csv([im[1],'未上传成功'],'file/un_upload_basic_info.csv')
            time.sleep(144)
            pass

# todaylist.T.to_csv('file/faver_stock_more_info.csv', index=False, sep=',')

# iter_stock_infomations('file/faver_stock.csv')