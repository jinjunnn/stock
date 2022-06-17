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
import ali_tablestore as ats


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

kkk = [['code', '001965']]

vvv = [('zip', '100022'), ('sector', 'Industrials'), ('fullTimeEmployees', 5459), ('longBusinessSummary', 'China Merchants Expressway Network & Technology Holdings Co.,Ltd. invests in and operates expressways in China. The company operates expressways under the Beijing-Tianjin-Tangshan Expressway, Yongtaiwen Expressway, Beilun Port Expressway, Jiurui Expressway, Guixing Expressway, Guiyang Expressway, Yangping Expressway, Guilin Lingsan Expressway, Edong Bridge, Chongqing-Guizhou Expressway, Shanghai-Chongqing Expressway, Bofu Expressway, and Guihuang Highway names. It is also involved in the traffic and ecology technology, and intelligent transportation businesses. The company was formerly known as China Merchants Huajian Highway Investment Co.,Ltd. and changed its name to China Merchants Expressway Network & Technology Holdings Co.,Ltd. in September 2016. The company was founded in 1965 and is based in Beijing, China. China Merchants Expressway Network & Technology Holdings Co.,Ltd. is a subsidiary of China Merchants Group Limited'), ('city', 'Beijing'), ('phone', '86 10 5652 9000'), ('country', 'China'), ('website', 'https://www.cmexpressway.com'), ('maxAge', 1), ('address1', 'China Merchants Office Building'), ('fax', '86 10 5652 9111'), ('industry', 'Infrastructure Operations'), ('address2', '31st Floor 118 Jianguo Road Chaoyang District'), ('ebitdaMargins', 0.52501), ('profitMargins', 0.57284), ('grossMargins', 0.40575), ('operatingCashflow', 4178541056), ('revenueGrowth', -0.101), ('operatingMargins', 0.3078), ('ebitda', 4425517568), ('targetLowPrice', 8.77), ('recommendationKey', 'strong_buy'), ('grossProfits', 3572929958), ('freeCashflow', 2303157248), ('targetMedianPrice', 9.05), ('currentPrice', 7.94), ('earningsGrowth', -0.117), ('currentRatio', 1.068), ('returnOnAssets', 0.01678), ('numberOfAnalystOpinions', 2), ('targetMeanPrice', 9.05), ('debtToEquity', 40.744), ('returnOnEquity', 0.085760005), ('targetHighPrice', 9.33), ('totalCash', 5892444160), ('totalDebt', 26169520128), ('totalRevenue', 8429357056), ('totalCashPerShare', 0.954), ('financialCurrency', 'CNY'), ('revenuePerShare', 1.301), ('quickRatio', 0.998), ('recommendationMean', 1.2), ('exchange', 'SHZ'), ('shortName', 'CHINA MERCHANTS EX'), ('longName', 'China Merchants Expressway Network & Technology Holdings Co.,Ltd.'), ('exchangeTimezoneName', 'Asia/Shanghai'), ('exchangeTimezoneShortName', 'CST'), ('isEsgPopulated', False), ('gmtOffSetMilliseconds', '28800000'), ('quoteType', 'EQUITY'), ('symbol', '001965.SZ'), ('messageBoardId', 'finmb_53474039'), ('market', 'cn_market'), ('enterpriseToRevenue', 8.823), ('enterpriseToEbitda', 16.805), ('52WeekChange', 0.0601604), ('forwardEps', 0.9), ('sharesOutstanding', 6178229760), ('bookValue', 9.57), ('lastFiscalYearEnd', 1640908800), ('heldPercentInstitutions', 0.07695), ('netIncomeToCommon', 4828667904), ('trailingEps', 0.702), ('lastDividendValue', 0.177), ('SandP52WeekChange', -0.0903551), ('priceToBook', 0.8296761), ('heldPercentInsiders', 0.87668), ('nextFiscalYearEnd', 1703980800), ('mostRecentQuarter', 1648684800), ('floatShares', 761899486), ('beta', 0.324), ('enterpriseValue', 74370670592), ('priceHint', 2), ('lastDividendDate', 1624579200), ('earningsQuarterlyGrowth', -0.117), ('priceToSalesTrailing12Months', 5.8195596), ('forwardPE', 8.822223), ('impliedSharesOutstanding', 0), ('previousClose', 7.93), ('regularMarketOpen', 7.92), ('twoHundredDayAverage', 7.6528), ('trailingAnnualDividendYield', 0.043631777), ('payoutRatio', 0.2522), ('regularMarketDayHigh', 8.03), ('averageDailyVolume10Day', 5870945), ('regularMarketPreviousClose', 7.93), ('fiftyDayAverage', 7.6946), ('trailingAnnualDividendRate', 0.346), ('open', 7.92), ('averageVolume10days', 5870945), ('dividendRate', 0.18), ('exDividendDate', 1624579200), ('regularMarketDayLow', 7.81), ('currency', 'CNY'), ('trailingPE', 11.310541), ('regularMarketVolume', 5685714), ('marketCap', 49055145984), ('averageVolume', 6223735), ('dayLow', 7.81), ('ask', 7.97), ('askSize', 0), ('volume', 5685714), ('fiftyTwoWeekHigh', 9.32), ('fiftyTwoWeekLow', 6.63), ('bid', 7.95), ('tradeable', False), ('dividendYield', 0.0221), ('bidSize', 0), ('dayHigh', 8.03), ('regularMarketPrice', 7.94), ('logo_url', 'https://logo.clearbit.com/cmexpressway.com')]


ats.put_row('stock',kkk,vvv)