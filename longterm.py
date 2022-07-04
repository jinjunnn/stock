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
def main(source_path,start_date,end_date):
    stock_list = open(source_path, 'r')
    reader = csv.reader(stock_list)
    _list = []
    for item in reader:
        try:
            df = sa.get_stock_data(item[1], start_date, end_date)
            # 设置鳄鱼线
            sa.add_alligator(df)
            sa.add_vegas(df)
            sa.add_bollinger(df)
            last_kline = df.iloc[-1]
            print(last_kline)
            show_plot = False
            image_url_bollinger = '/Users/pharaon/Downloads/bollinger/{}.png'.format(str(time.time()))
            image_url_longterm = '/Users/pharaon/Downloads/longterm/{}.png'.format(str(time.time()))
            mp.plot_longterm(df,item[1],show_plot,image_url_longterm) if last_kline['alligator_crossover'] == 1 else None
            mp.plot_longterm(df,item[1],show_plot,image_url_bollinger) if last_kline['bollinger_crossover'] == 1 else None
            if show_plot == False:
                time.sleep(1)
        except Exception as e:
            print(e)

# 定义一个主函数
if __name__ == '__main__':
    start_date = common.today_int_shift(300)
    end_date = common.today_int()
    main('/Users/pharaon/Project/stock/file/total.csv',start_date,end_date)
    # pass

    


