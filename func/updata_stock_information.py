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
import tg

def prepare_data(code,stock):
    for key in list(stock.keys()):
        if stock[key] == None:
            stock.pop(key)
    # 去掉这个值是列表的字段
    stock['companyOfficers'] = ''
    stock.pop('companyOfficers')

    primary_key = [['code', sf.remove_suffix(code)]]
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

iter_stocks('/Users/pharaon/Project/stock/file/total.csv')












        # try:
        #     stock = ats.get_row('stock',[('code',sf.remove_suffix(item[1]))],['totalCash'])
        #     print(stock)
        #     print(stock.primary_key,stock.attribute_columns)
        # except  Exception as e:
        #     print(e)



        # try:
        #     stock = get_stock_infomations(item[1])
        # except  Exception as e:
        #     print(e)

        # try:
        #     response = alt.put_row('stock',[('code',sf.remove_suffix(item[1]))],[('askSize',0)])
        #     print(response)
        # except Exception as e:
        #     print(e)




# stock = ats.get_row('stock',[('code','000416')],['totalCash'])
# print(stock)

# _list = ['1','2','3'] 
# result = ' '.join(_list)
# print(result)


# proxy_list = pf.proxy['data']
# for item in proxy_list:
#     proxyMeta = "http://%(host)s:%(port)s" % {
#         "host" : item['ip'],
#         "port" : item['port'],
#     }
#     proxies = {
#         "http"  : proxyMeta,
#         "https"  : proxyMeta
#     }
#     print(proxies)


# proxyMeta = "http://%(host)s:%(port)s" % {
#     "host" : '175.174.186.98',
#     "port" : '4251',
# }
# proxies = {
#     "http"  : proxyMeta,
#     "https"  : proxyMeta
# }
# print(proxies)
# tickers = yf.Tickers('000877.SZ 002064.SZ')
# for ticker in tickers.tickers:
#     # prepare_data(ticker,tickers.tickers[ticker].get_cashflow(proxy=proxies))
#     result = ticker,tickers.tickers[ticker].get_cashflow(proxy=proxies)
#     print(result)





# print(tickers.tickers['000877.SZ'].info)

# {'zip': '325206', 'sector': 'Basic Materials', 'fullTimeEmployees': 7395, 'longBusinessSummary': 'Huafon Chemical Co., Ltd. produces and sells spandex in China. It offers Qianxi spandex yarn, a PU elastic fiber for use in the fields of underwear, swimming suits, socks, jeans, leisure sportswear, medical bandage, fabric ribbon, diapers, etc. It is also involved in producing cyclohexanone, as well as other benzene related products; the import and export of textile products, such as spandex fiber; and dealing with power and heat cogeneration business. The company was formerly known as Zhejiang Huafeng Spandex Co., Ltd. and changed its name to Huafon Chemical Co., Ltd. in January 2021. Huafon Chemical Co., Ltd. was founded in 1999 and is headquartered in Ruian, China.', 'city': 'Ruian', 'phone': '86 577 6515 0000', 'country': 'China', 'companyOfficers': [], 'website': 'https://www.huafeng.com', 'maxAge': 1, 'address1': 'No. 1788, Kaifaqu Road', 'fax': '86 577 6553 7858', 'industry': 'Specialty Chemicals', 'address2': 'Economic Development Zone', 'ebitdaMargins': 0.32860002, 'profitMargins': 0.25643998, 'grossMargins': 0.36366, 'operatingCashflow': 6028673536, 'revenueGrowth': 0.259, 'operatingMargins': 0.29532, 'ebitda': 9813904384, 'targetLowPrice': 12, 'recommendationKey': 'strong_buy', 'grossProfits': 10978326068, 'freeCashflow': 2273349632, 'targetMedianPrice': 12, 'currentPrice': 8, 'earningsGrowth': -0.171, 'currentRatio': 2.537, 'returnOnAssets': 0.20071, 'numberOfAnalystOpinions': 1, 'targetMeanPrice': 12, 'debtToEquity': 13.893, 'returnOnEquity': 0.42130002, 'targetHighPrice': 12, 'totalCash': 10170114048, 'totalDebt': 3214994944, 'totalRevenue': 29865967616, 'totalCashPerShare': 2.049, 'financialCurrency': 'CNY', 'revenuePerShare': 6.431, 'quickRatio': 1.928, 'recommendationMean': 1.4, 'exchange': 'SHZ', 'shortName': 'HUAFON CHEMICAL CO', 'longName': 'Huafon Chemical Co., Ltd.', 'exchangeTimezoneName': 'Asia/Shanghai', 'exchangeTimezoneShortName': 'CST', 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '28800000', 'quoteType': 'EQUITY', 'symbol': '002064.SZ', 'messageBoardId': 'finmb_28390091', 'market': 'cn_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 1.088, 'beta3Year': None, 'enterpriseToEbitda': 3.312, '52WeekChange': -0.336394, 'morningStarRiskRating': None, 'forwardEps': 1.36, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': 4962540032, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'totalAssets': None, 'bookValue': 4.663, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': None, 'lastFiscalYearEnd': 1640908800, 'heldPercentInstitutions': 0.090450004, 'netIncomeToCommon': 7658957312, 'trailingEps': 1.649, 'lastDividendValue': 0.3, 'SandP52WeekChange': -0.11992943, 'priceToBook': 1.7156336, 'heldPercentInsiders': 0.66916, 'nextFiscalYearEnd': 1703980800, 'yield': None, 'mostRecentQuarter': 1648684800, 'shortRatio': None, 'sharesShortPreviousMonthDate': None, 'floatShares': 1667265873, 'beta': 1.335217, 'enterpriseValue': 32499595264, 'priceHint': 2, 'threeYearAverageReturn': None, 'lastSplitDate': 1433116800, 'lastSplitFactor': '20:10', 'legalType': None, 'lastDividendDate': 1654732800, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': -0.169, 'priceToSalesTrailing12Months': 1.3292829, 'dateShortInterest': None, 'pegRatio': None, 'ytdReturn': None, 'forwardPE': 5.882353, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 'impliedSharesOutstanding': 0, 'category': None, 'fiveYearAverageReturn': None, 'previousClose': 7.95, 'regularMarketOpen': 7.9, 'twoHundredDayAverage': 10.1594, 'trailingAnnualDividendYield': 0.03773585, 'payoutRatio': 0.060599998, 'volume24Hr': None, 'regularMarketDayHigh': 8.02, 'navPrice': None, 'averageDailyVolume10Day': 23528430, 'regularMarketPreviousClose': 7.95, 'fiftyDayAverage': 8.1318, 'trailingAnnualDividendRate': 0.3, 'open': 7.9, 'toCurrency': None, 'averageVolume10days': 23528430, 'expireDate': None, 'algorithm': None, 'dividendRate': 0.3, 'exDividendDate': 1654732800, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 7.82, 'currency': 'CNY', 'trailingPE': 4.851425, 'regularMarketVolume': 16332436, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': 39700320256, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 19928602, 'dayLow': 7.82, 'ask': 8, 'askSize': 0, 'volume': 16332436, 'fiftyTwoWeekHigh': 15.76, 'fromCurrency': None, 'fiveYearAvgDividendYield': None, 'fiftyTwoWeekLow': 7.28, 'bid': 7.99, 'tradeable': False, 'dividendYield': 0.0377, 'bidSize': 0, 'dayHigh': 8.02, 'regularMarketPrice': 8, 'preMarketPrice': None, 'logo_url': 'https://logo.clearbit.com/huafeng.com'}

# {'zip': '830013', 'sector': 'Basic Materials', 'fullTimeEmployees': 70829, 'longBusinessSummary': 'Xinjiang Tianshan Cement Co., Ltd. produces and sells cement, clinker, and commercial concrete in China and internationally. It offers Portland cement and ordinary Portland cement, as well as special cements, such as oil wells, anti-sulfur, and low-to-medium heat cements, which are used in various construction projects, including industry, agriculture, water conservancy, transportation, civil and municipal, etc. The company also provides pre-stressed and self-stressed reinforced concrete components; and conventional commercial concrete and high-strength concrete for engineering projects, such as ordinary buildings, high-rise buildings, highways, tunnels, viaducts, subways, and underground mines. It is also involved in the waste heat power generation business. The company was founded in 1998 and is based in Urumqi, China.', 'city': 'Urumqi', 'phone': '86 99 1668 6791', 'country': 'China', 'companyOfficers': [], 'website': 'https://www.sinoma-tianshan.cn', 'maxAge': 1, 'address1': 'Tianhe Building', 'fax': '86 99 1668 6782', 'industry': 'Building Materials', 'address2': 'No. 1256, Hebei East Road', 'ebitdaMargins': 0.20977, 'profitMargins': 0.07209, 'grossMargins': 0.24239, 'operatingCashflow': 27467440128, 'revenueGrowth': -0.018, 'operatingMargins': 0.15574001, 'ebitda': 35550556160, 'targetLowPrice': 15.21, 'recommendationKey': 'strong_buy', 'grossProfits': 42374935091, 'freeCashflow': 42991321088, 'targetMedianPrice': 15.3, 'currentPrice': 12.03, 'earningsGrowth': -0.28, 'currentRatio': 0.576, 'returnOnAssets': 0.10568, 'numberOfAnalystOpinions': 3, 'targetMeanPrice': 15.39, 'debtToEquity': 93.266, 'returnOnEquity': 0.26734, 'targetHighPrice': 15.66, 'totalCash': 21377546240, 'totalDebt': 90198458368, 'totalRevenue': 169470230528, 'totalCashPerShare': 2.468, 'financialCurrency': 'CNY', 'revenuePerShare': 20.841, 'quickRatio': 0.466, 'recommendationMean': 1.4, 'exchange': 'SHZ', 'shortName': 'XINJIANG T/SHAN CE', 'longName': 'Xinjiangtianshan Cement Co.,Ltd', 'exchangeTimezoneName': 'Asia/Shanghai', 'exchangeTimezoneShortName': 'CST', 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '28800000', 'quoteType': 'EQUITY', 'symbol': '000877.SZ', 'messageBoardId': 'finmb_5722115', 'market': 'cn_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 1.108, 'beta3Year': None, 'enterpriseToEbitda': 5.282, '52WeekChange': -0.11816841, 'morningStarRiskRating': None, 'forwardEps': 1.8, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': 8663419904, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'totalAssets': None, 'bookValue': 9.374, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': None, 'lastFiscalYearEnd': 1640908800, 'heldPercentInstitutions': 0.00751, 'netIncomeToCommon': 12217751552, 'trailingEps': 1.502, 'lastDividendValue': 0.33, 'SandP52WeekChange': -0.11992943, 'priceToBook': 1.2833369, 'heldPercentInsiders': 0.91189003, 'nextFiscalYearEnd': 1703980800, 'yield': None, 'mostRecentQuarter': 1648684800, 'shortRatio': None, 'sharesShortPreviousMonthDate': None, 'floatShares': 1090724932, 'beta': 0.882173, 'enterpriseValue': 187761147904, 'priceHint': 2, 'threeYearAverageReturn': None, 'lastSplitDate': 1337126400, 'lastSplitFactor': '18:10', 'legalType': None, 'lastDividendDate': 1654646400, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': -0.234, 'priceToSalesTrailing12Months': 0.6149808, 'dateShortInterest': None, 'pegRatio': 0.12, 'ytdReturn': None, 'forwardPE': 6.6833334, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 'impliedSharesOutstanding': 0, 'category': None, 'fiveYearAverageReturn': None, 'previousClose': 11.94, 'regularMarketOpen': 11.88, 'twoHundredDayAverage': 13.9635, 'trailingAnnualDividendYield': 0.027638193, 'payoutRatio': 0.31620002, 'volume24Hr': None, 'regularMarketDayHigh': 12.03, 'navPrice': None, 'averageDailyVolume10Day': 16145088, 'regularMarketPreviousClose': 11.94, 'fiftyDayAverage': 12.489, 'trailingAnnualDividendRate': 0.33, 'open': 11.88, 'toCurrency': None, 'averageVolume10days': 16145088, 'expireDate': None, 'algorithm': None, 'dividendRate': 0.33, 'exDividendDate': 1654646400, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 11.81, 'currency': 'CNY', 'trailingPE': 8.009321, 'regularMarketVolume': 12283554, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': 104220942336, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 16420909, 'dayLow': 11.81, 'ask': 12.04, 'askSize': 0, 'volume': 12283554, 'fiftyTwoWeekHigh': 18.44, 'fromCurrency': None, 'fiveYearAvgDividendYield': 2.34, 'fiftyTwoWeekLow': 11.48, 'bid': 12.03, 'tradeable': False, 'dividendYield': 0.0276, 'bidSize': 0, 'dayHigh': 12.03, 'regularMarketPrice': 12.03, 'preMarketPrice': None, 'logo_url': 'https://logo.clearbit.com/sinoma-tianshan.cn'}