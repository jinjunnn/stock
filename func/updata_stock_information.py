import csv



def iter_stocks():
    #打开csv文件
    
    # stock_list = open('file/stock_list.csv', 'r')
    # reader = csv.reader(stock_list)
    
    stock_list = open('/Users/pharaon/Project/stock/file/total.csv', 'r')
    reader = csv.reader(stock_list)
    for item in reader:
        print(item)
        # try:
        #     response = alt.put_row('stock',[('code',sf.remove_suffix(item[1]))],[('askSize',0)])
        #     print(response)
        # except Exception as e:
        #     print(e)

iter_stocks()