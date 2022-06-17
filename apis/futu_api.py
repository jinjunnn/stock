from futu import *
import csv

import apis.stock_formula as sf


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

    ret, data = quote_ctx.get_plate_list(Market.SZ, Plate.ALL)
    if ret == RET_OK:
        print(data)
        print(data['plate_name'][0])    # 取第一条的板块名称
        print(data['plate_name'].values.tolist())   # 转为 list
    else:
        print('error:', data)
    quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽




# 修改自选股列表
def upload_stock_to_futu(resource_path,futu_stock_list_name):
    stock_list = open(resource_path, 'r')
    reader = csv.reader(stock_list)
    for item in reader:
        time.sleep(5)
        stock_name = sf.modify_stockcode(item[1])
        print([stock_name])
        modify_favor(futu_stock_list_name,[stock_name])



# upload_stock_to_futu('file/faver.csv','绩优股')


# get_market()

# 富途股票订阅
# def futu_subscribe(stocklist):
#     quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
#     ret, data = quote_ctx.subscribe(stocklist, SubType.QUOTE)
#     if ret == RET_OK:
#         print(data)
#     else:
#         print('error:', data)
#     quote_ctx.close()

# result = futu_subscribe(['SZ.000019'])
# print(result)


# modify_favor('A',['HK.00700','SZ.000019'])

# class PriceReminderTest(PriceReminderHandlerBase):
#     def on_recv_rsp(self, rsp_pb):
#         ret_code, content = super(PriceReminderTest,self).on_recv_rsp(rsp_pb)
#         if ret_code != RET_OK:
#             print("PriceReminderTest: error, msg: %s" % content)
#             return RET_ERROR, content
#         print("PriceReminderTest ", content) # PriceReminderTest 自己的处理逻辑
#         return RET_OK, content
        
# quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
# handler = PriceReminderTest()
# quote_ctx.set_handler(handler)  # 设置到价提醒通知回调
# time.sleep(15)  # 设置脚本接收 FutuOpenD 的推送持续时间为15秒
# quote_ctx.close()   # 关闭当条连接，FutuOpenD 会在1分钟后自动取消相应股票相应类型的订阅