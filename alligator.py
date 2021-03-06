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
import common

# 设置条件，将符合条件的股票上传到富途证券APP
def doit(code, start_date, end_date):
    try:
        df = sa.get_stock_data(code, start_date, end_date)
        # 设置鳄鱼线
        sa.add_alligator(df)
        sa.add_vegas(df)
        sa.add_bollinger(df)
        mp.plot_longterm(df,code,True,True)
        main()
    except Exception as e:
        print(e)
        main()

def main():
    start_date = common.today_int_shift(300)
    end_date = common.today_int()

    code_row = input('input code = ')
    code = common.add_stockcode_suffix(str(code_row))
    print(code)
    doit(code, start_date, end_date)

# 定义一个主函数
if __name__ == '__main__':
    main()