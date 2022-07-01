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
            last_kline = df.iloc[-1]
            
            # df.to_csv('/Users/pharaon/Project/stock/stock/test_total.csv')
            show_plot = False
            mp.plot_alligator(df,item[1],show_plot) if last_kline['alligator_crossover'] == 1 else None
            time.sleep(1) if show_plot == False else None
        except Exception as e:
            print(e)

# 定义一个主函数
if __name__ == '__main__':
    start_date = common.today_int_shift(300)
    end_date = common.today_int()
    main('/Users/pharaon/Project/stock/file/total.csv',start_date,end_date)
    # pass

    


