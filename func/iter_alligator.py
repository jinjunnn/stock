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
            print(df)
            mp.plot_alligator(df,item[1])
        except Exception as e:
            print(e)

# 定义一个主函数
if __name__ == '__main__':
    start_date = sf.today_int_shift(1000)
    end_date = sf.today_int()
    main('/Users/pharaon/Project/stock/file/total.csv',start_date,end_date)
    # pass

    


