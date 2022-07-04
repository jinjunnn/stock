#  输入股票信息输出一年内股票每日最大振幅


import sys
sys.path.append("./apis")
import stock_api as sa
import common

def other_stock():
    code_row = input('input code = ')
    code = common.add_stockcode_suffix(code_row)
    get_stock(code)

def get_stock(code):
    try:
        start_date = common.today_int_shift(365)
        end_date = common.today_int()
        df = sa.get_stock_data(code, start_date, end_date)
        a = ((df['high'] - df['low']) / df['low']).mean() * 100
        print(round(a, 2))
        other_stock()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    code_row = input('input code = ')
    code = common.add_stockcode_suffix(code_row)
    get_stock(code)