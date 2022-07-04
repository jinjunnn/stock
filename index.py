# 查询指数的信息
#

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import pandas_ta as pa
import csv
import time

import sys
sys.path.append("./apis")
import stock_api as sa
import matplot as mp
import common

# 设置条件，将符合条件的股票上传到富途证券APP

# 查询指数列表
def get_index_list(market):
    sa.get_index_list(market)
    print('completed')
# get_index_list('SW')

def main(df,index_title,image_url):
    try:
        sa.add_alligator(df)
        sa.add_vegas(df)
        print(df.iloc[-1])
        sa.add_bollinger(df)
        mp.plot_longterm(df,index_title,True,image_url)
    except Exception as e:
        print(e)

# 定义一个主函数
if __name__ == '__main__':

    code = input('input full code = ')

    start_date = common.today_int_shift(300)
    end_date = common.today_int()
    image_url =  None   #'/Users/pharaon/Downloads/index/{}.png'.format(str(time.time())) # 如果是下载需要给一个下载的地址，如果是直接打开绘图工具不需要
    df = sa.get_index_daily(code, start_date=start_date, end_date=end_date)
    print(df)
    main(df,code,image_url)