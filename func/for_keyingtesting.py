import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import sys
sys.path.append("./apis")
import stock_api as sa
import matplot as mp


ts_code = '513050.SH'
start_date = 20220101
end_date = 20220617

stock = sa.fund_bollinger_bands_strategy(ts_code=ts_code, start_date=start_date, end_date=end_date)
print(stock)
mp.plot_boolinger(stock, 'for keying testing')