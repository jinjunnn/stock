from futu import *
import csv
import datetime
import pandas_ta as pa
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.pyplot import MultipleLocator
import telebot

api_key = '5326945934:AAHhxIoe08JaW7wNi1nGsInUcbq5MeOieOE'
bot = telebot.TeleBot(api_key, parse_mode=None) 

def stoch(stock,row,timeperiod,_key):
    try:
        result = stock.loc[row.name - timeperiod:row.name-1, _key]
        _max = result.max()
        _min = result.min()
        _current = row.loc[_key]
        i = (_current - _min) / (_max - _min) if (_max - _min) != 0 else 0
        return i
    except:
        pass

def send_photo(chat_id,url):
    photo = open(url, 'rb')
    bot.send_photo(chat_id, photo)

def send_text(chat_id,text):
    bot.send_message(chat_id, text)

def plot_boolinger(df,stock_code,image_url,last_kline):
    table_title = 'Important ***{}-- {}'.format(stock_code,last_kline['time_key']) if last_kline['close_crossover_ema'] == 1 and last_kline['macd_crossover_signal'] == 1 else ('macd crossover signal--{}--{}'.format(stock_code,last_kline['time_key']) if last_kline['macd_crossover_signal'] == 1 else '{}--{}'.format(stock_code,last_kline['time_key']))
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(df['time_key'], df['hlc3'],label='hlc3')
    axs[0].plot(df['time_key'], df['ema_upper'],label='boollinger_upper')
    axs[0].plot(df['time_key'], df['ema_lower'],label='boollinger_lower')
    axs[0].plot(df['time_key'], df['ema'],label='boollinger_middle')
    axs[0].set_ylabel('Price')
    axs[0].set_title(table_title)
    #设置时间刻度
    axs[0].xaxis.set_major_locator(MultipleLocator(40))
    # axs[0].text(0.95, 0.01, 'colored text in axes coords',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes,fontsize=12)
    # ax.invert_xaxis() # 切换X轴方向
    # axs[0].legend() # 设置图标标注说明

    axs[1].bar(df['time_key'], df['volume'],label='volume')
    #设置时间刻度
    axs[1].xaxis.set_major_locator(MultipleLocator(40))

    axs[2].plot(df['time_key'], df['spike'],label='spike')
    axs[2].plot(df['time_key'], df['spike_upper'],label='spike_upper')
    axs[2].plot(df['time_key'], df['spike_lower'],label='spike_lower')
    # axs[2].legend()
    #设置时间刻度
    axs[2].xaxis.set_major_locator(MultipleLocator(40))

    axs[3].plot(df['time_key'], df['macd'],label='macd')
    axs[3].plot(df['time_key'], df['signal'],label='signal')
    axs[3].bar(df['time_key'], df['histogram'],label='histogram')
    # axs[3].legend()
    axs[3].xaxis.set_major_locator(MultipleLocator(40))
    plt.savefig(image_url,dpi=800)
    # plt.show()


def add_bollinger(df):
    timeperiod = 20
    try:
        df['hlc3'] = pa.hlc3(df['high'], df['low'], df['close'])
        bbands = pa.bbands(df['hlc3'],length = timeperiod, std=2, mamode="ema", ddof = 0)
        df['ema_lower'] = bbands['BBL_20_2.0']
        df['ema'] = bbands['BBM_20_2.0']
        df['ema_upper'] = bbands['BBU_20_2.0']
        df['bandwidth'] = bbands['BBB_20_2.0']
        df['bandwidth_chg'] = df['bandwidth'] - bbands['BBB_20_2.0'].shift()
        df['percent'] = bbands['BBP_20_2.0']
        df['close_crossover_ema'] = pa.cross(df['close'],df['ema']) # 收盘价穿越 中线

        # 震荡指标 valotility oscillator 
        df['spike'] = df['close'] - df['open']
        df['spike_upper'] = pa.stdev(df['spike'], length = 100, ddof = 0)
        df['spike_lower'] = -pa.stdev(df['spike'], length = 100, ddof = 0)

        # df['ema'] = pa.ema(df['hlc3'],length=20)
        macd = pa.macd(df['hlc3'],fast=12,slow=26,signal=9)
        df['macd'] = macd['MACD_12_26_9']/ df['ema'] * 100
        df['histogram'] = macd['MACDh_12_26_9']/ df['ema'] * 100
        df['signal']=macd['MACDs_12_26_9']/ df['ema'] * 100
        df['hist_below'] = pa.below(df['histogram'], df['histogram'].shift())
        df['hsit_below_shift'] = df['hist_below'].shift()
        df['hist_signal'] = df.apply(lambda x: 1 if x['hsit_below_shift'] == 1 and x['hist_below'] == 0 else (-1 if x['hsit_below_shift'] == 0 and x['hist_below'] == 1 else 0),axis=1)
        df['macd_crossover_signal'] = pa.cross(df['macd'],df['signal']) # 收盘价穿越 中线
        df['stoch'] = df.apply(lambda x:stoch(df, x, 5, 'close'), axis=1) # 前5只k线 的位置

        df = df.fillna(value=0)
        return df[20:]
    except Exception as e:
        print(e)
        return None

# 将股票代码和股票交易所翻转, 如: 600000.SH -> SH.600000
def modify_stockcode(stock_code):
    if stock_code[0] == '6':
        return 'SH.' + stock_code[0:6]
    else:
        return 'SZ.' + stock_code[0:6]


# 修改自选股列表
def modify_favor(name, stocklist):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    try:
        ret, data = quote_ctx.modify_user_security(name, ModifyUserSecurityOp.ADD, stocklist)
        if ret == RET_OK:
            print(data) # 返回 success
        else:
            print('error:', data)
        quote_ctx.close() # 结束后记得关闭当条连接
    except print('失败'):
        pass

# 获取板块数据
def get_market():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.get_plate_list(Market.SH, Plate.ALL)
    if ret == RET_OK:
        print(data)
        #保存df到csv文件
        # # data.to_csv('./file/sH_plate.csv', index=False)
        # print(data['plate_name'][0])    # 取第一条的板块名称
        # print(data['plate_name'].values.tolist())   # 转为 list
    else:
        print('error:', data)
    quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽


# 获得某个板块下的股票清单
def get_stocks_in_market(plate):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.get_plate_stock(plate)
    if ret == RET_OK:
        print(data)

    else:
        print('error:', data)
    quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
# get_stocks_in_market('SH.BK0784')

# 修改自选股列表，列表的名字必须已经设定好
def upload_stock_to_futu(resource_path,futu_stock_list_name):
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    for item in reader:
        time.sleep(5)
        stock_name = modify_stockcode(item[1])
        print([stock_name])
        modify_favor(futu_stock_list_name,[stock_name])
        
# upload_stock_to_futu('file/faver.csv','绩优股')


# 富途股票订阅
def subscribe(stocklist):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.subscribe(stocklist, SubType.QUOTE)
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
    quote_ctx.close()

# result = futu_subscribe(['SZ.000960'])
# print(result)

# 查询订阅数量
def query_subscribe():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.query_subscription()
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
    quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽

def unsubscribe():
    pass


# 获取历史k线数据,必须中国 IP 才可以获得这个权限。
def get_history_kline(stocklist,ktype,start_date, end_date):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data, page_req_key = quote_ctx.request_history_kline(stocklist, start=start_date, end=end_date, ktype=ktype,max_count=1000,autype=AuType.QFQ)  # 每页5个，请求第一页
    if ret == RET_OK:
        quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
        return data
    else:
        print('error:', data)
        quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽

# result = get_history_kline('SZ.000960', 'K_15M','2021-06-01','2021-09-01')
# print(result)


def get_realtime_kline(stocklist, ktype, start_date, end_date,amount):
    # amount 是 k线的数量
    subscribe_type = [SubType.K_30M] if ktype == 30 else ([SubType.K_15M] if ktype == 15 else ([SubType.K_5M] if ktype == 5 else [SubType.K_60M])) # 设置 K线时间长度
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_unsub, err_message_unsub = quote_ctx.unsubscribe_all()  # 取消所有订阅
    if ret_unsub == RET_OK:#  先取消所有历史订阅，防止连接条数用尽
        ret_sub, err_message = quote_ctx.subscribe(stocklist, subscribe_type, subscribe_push=False) # 订阅
        for i in range(25):
            if ret_sub == RET_OK:  # 订阅成功
                for item in stocklist:
                    # print(item)
                    ret, data = quote_ctx.get_cur_kline(item, amount, subscribe_type[0], AuType.QFQ)  # 获取港股00700最近2个 K 线数据
                    if ret == RET_OK:
                        try:
                            df = add_bollinger(data)
                            last_kline = df.iloc[-1]
                            if last_kline['spike'] > last_kline['spike_upper']:
                                image_url = '/Users/pharaon/Downloads/stock/{}.png'.format(str(time.time()))
                                print(last_kline)
                                plot_boolinger(df,item,image_url,last_kline)#绘制并存储表格
                                # send_photo(2013737722,image_url)#将绘制的表格发送到TG
                                # send_text(2013737722, last_kline.to_string())
                            # print(data['turnover_rate'][0])   # 取第一条的换手率
                            # print(data['turnover_rate'].values.tolist())   # 转为 list
                            if last_kline['macd_crossover_signal']==1:
                                image_url = '/Users/pharaon/Downloads/shortterm/{}.png'.format(str(time.time()))
                                plot_boolinger(df,item,image_url,last_kline)#绘制并存储表格
                                # send_photo(2013737722,image_url)#将绘制的表格发送到TG
                                # send_text(2013737722, last_kline.to_string())
                            if last_kline['hist_signal']== 1 and last_kline['histogram'] < 0:
                                # 如果 MACD 在 0 线以下，并且前一个macd 下降，当前macd 上升，并且比率足够大。
                                image_url = '/Users/pharaon/Downloads/shortterm/{}.png'.format(str(time.time()))
                                plot_boolinger(df,item,image_url,last_kline)#绘制并存储表格
                                # send_photo(2013737722,image_url)#将绘制的表格发送到TG
                        except Exception as e:
                            print(e)
                    else:
                        print('error:', data)
                send_text(2013737722, '遍历结束，请查收')
            else:
                print('subscription failed', err_message)
            time.sleep( ktype * 20 )
    else:
        print('Failed to cancel all subscriptions！', err_message_unsub)
    quote_ctx.close()  # 关闭当条连接，FutuOpenD 会在1分钟后自动取消相应股票相应类型的订阅




