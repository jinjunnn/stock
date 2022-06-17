import leancloud

#lc国际版
leancloud.init(
    "SpLCjLUgNCMtfbwH60NFu0pi-MdYXbMMI", master_key="01Khh0a2u4KAX274WKwYm8Bm")

def upload_information(stock_name, stock_info):
    # 创建一个新的对象
    StockInfo = leancloud.Object.extend('StockInfo')
    stock_info_object = StockInfo()
    stock_info_object.set("stock_code", stock_name)
    for key, value in stock_info.items():
        stock_info_object.set(key, value)
    stock_info_object.save()
# stock_name = '000960.SZ'
# stock_info = {
#     'trailingEps': '0.00',
#     'targetLowPrice': '0.00',
#     'targetMeanPrice': '0.00',
#     'targetMedianPrice': '0.00',
#     'targetHighPrice': '0.00'
# }

# upload_information(stock_name, stock_info)

def print_api():
    print('leancloud')