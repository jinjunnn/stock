import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import sys
sys.path.append("./apis")
import stock_api as sa
import matplot as mp
import common


ts_code = '513050.SH'
start_date = common.today_int_shift(300)
end_date = common.today_int()

stock = sa.fund_bollinger_bands_strategy(ts_code=ts_code, start_date=start_date, end_date=end_date)
print(stock)
mp.plot_candle(stock, ts_code)