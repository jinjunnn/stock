#通过鳄鱼线指标来寻找中长线的交易机会，然后通过布林带策略在趋势股中不断做短线的交易策略
#

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import pandas_ta as pa
import csv

import sys
sys.path.append("./apis")
import stock_api as sa
import matplot as mp
import stock_formula as sf

# 设置条件，将符合条件的股票上传到富途证券APP

# 查询指数列表
def get_index_list(market):
    sa.get_index_list(market)
    print('completed')
# get_index_list('SW')


def main(df):
    try:
        sa.add_alligator(df)
        sa.add_vegas(df)
        print(df.iloc[-1])
        mp.plot_alligator(df,code)
    except Exception as e:
        print(e)

# 定义一个主函数
if __name__ == '__main__':
    code = '000043.SH'
    start_date = sf.today_int_shift(1000)
    end_date = sf.today_int()
    df = sa.get_index_daily(code, start_date=start_date, end_date=end_date)
    print(df)
    main(df)