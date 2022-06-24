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
def main(code, start_date, end_date):
    try:
        df = sa.get_stock_data(code, start_date, end_date)
        # 设置鳄鱼线
        sa.add_alligator(df)
        sa.add_vegas(df)
        print(df.iloc[-1])
        mp.plot_alligator(df,code)
    except Exception as e:
        print(e)

# 定义一个主函数
if __name__ == '__main__':
    start_date = sf.today_int_shift(300)
    end_date = sf.today_int()
    main('000960.SZ', start_date, end_date)
