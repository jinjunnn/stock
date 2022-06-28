from futu import *
import csv
import datetime
import pandas_ta as pa
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.pyplot import MultipleLocator
import telebot

api_key = '5326945934:AAG0AYlJvGI40v9dpFHcvN64gliDDzkqGQI'
bot = telebot.TeleBot(api_key, parse_mode=None) 


def modify_stocklist(stocklist):
    _list = []
    for item in stocklist:
        if item[0] == '6':
            _list.append('SH.' + item[0:6]) 
        else:
            _list.append('SZ.' + item[0:6])
    return _list

#字符串类型的数据，用于查询富途数据
def date_shift(days):
    return (datetime.datetime.now()-datetime.timedelta(days=days)).strftime('%Y-%m-%d')

#字符串类型的数据，用于查询富途数据
def today():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def send_photo(chat_id,url):
    photo = open(url, 'rb')
    bot.send_photo(chat_id, photo)

def send_text(chat_id,text):
    bot.send_message(chat_id, text)

def plot_boolinger(df,stock_code,image_url):
    last_kline = df.iloc[-1]
    table_title = 'Important ***{}-- {}'.format(stock_code,last_kline['time_key']) if last_kline['close_crossover_ema'] == 0 and last_kline['close_crossover_ema'] == 0 else '{}--{}'.format(stock_code,last_kline['time_key'])
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
        df['macd'] = macd['MACD_12_26_9']
        df['histogram'] = macd['MACDh_12_26_9']
        df['signal']=macd['MACDs_12_26_9']
        df['macd_crossover_signal'] = pa.cross(df['macd'],df['signal']) # 收盘价穿越 中线

        df = df.fillna(value=0)
        return df[20:]
    except Exception as e:
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
                    print(item)
                    ret, data = quote_ctx.get_cur_kline(item, amount, subscribe_type[0], AuType.QFQ)  # 获取港股00700最近2个 K 线数据
                    if ret == RET_OK:
                        df = add_bollinger(data)
                        last_kline = df.iloc[-1]
                        if last_kline['spike'] > last_kline['spike_upper']:
                            image_url = '/Users/pharaon/Downloads/stock/{}.png'.format(str(time.time()))
                            print(last_kline)
                            plot_boolinger(df,item,image_url)#绘制并存储表格
                            send_photo(2013737722,image_url)#将绘制的表格发送到TG
                            send_text(2013737722, last_kline.to_string())
                        # print(data['turnover_rate'][0])   # 取第一条的换手率
                        # print(data['turnover_rate'].values.tolist())   # 转为 list
                    else:
                        print('error:', data)
            else:
                print('subscription failed', err_message)
            time.sleep( ktype * 20 )
    else:
        print('Failed to cancel all subscriptions！', err_message_unsub)
    quote_ctx.close()  # 关闭当条连接，FutuOpenD 会在1分钟后自动取消相应股票相应类型的订阅


if __name__ == '__main__':
    stocklist = ['000960','603938','002518','002463','603707','603939','003019','603218','000999','603883','002245','002960','600885','000708','601869','002984','002765','601677','000959','603808','600426','300681','300662','300136','301050','300687','300815','300984','300218','301191','300791','301058','301040','301099','300638','301221','300432','301092','300196','300395','300777','300759','300776','300476','300628','300390','300672','300482','300122','300014','300316','300496','300604','300502','300763','300775','300750','300244','300363','002989','603039','601882','002585','603113','600765','003029','002960','002649','002648','603663','002915','002968','603233','002859','605066','002009','002335','603588','603877','605090','605398','002191','002008','603565','600782','601677','000811','002978','002886','601163','002429','605189','603678','600150','600282','600038','603809','600729','603587','605060']
    ktype = 15
    start_date = date_shift(60)
    end_date = today()
    amount = 300
    get_realtime_kline(modify_stocklist(stocklist),ktype,start_date,end_date,amount)



