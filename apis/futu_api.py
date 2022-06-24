from futu import *
import csv

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
def futu_subscribe(stocklist):
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
def query_futu_subscribe():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.query_subscription()
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
    quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽


# 获取历史k线数据,必须中国 IP 才可以获得这个权限。
def get_history_kline(stock_code,ktype,start_date, end_date):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data, page_req_key = quote_ctx.request_history_kline(stock_code, start=start_date, end=end_date, ktype=ktype,max_count=1000,autype=AuType.QFQ)  # 每页5个，请求第一页
    if ret == RET_OK:
        quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
        return data
    else:
        print('error:', data)

result = get_history_kline('SZ.000960', 'K_15M','2021-06-01','2021-09-01')
