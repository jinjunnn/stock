# -*- coding: utf8 -*-
from tablestore import *
import time

import stock_formula as sf

client = OTSClient("https://pharaontrade.cn-hangzhou.ots.aliyuncs.com", 'LTAI5tLWK2gTt8JB3kHkxyCa', 'xzlgVf6tbFBm3yNpUL54GnhdAi6oML', 'pharaontrade')

def create_table(client, table_name):
    schema_of_primary_key = [('gid', 'INTEGER'), ('uid', 'INTEGER')]
    table_meta = TableMeta(table_name, schema_of_primary_key)
    table_option = TableOptions()
    reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
    client.create_table(table_meta, table_option, reserved_throughput)
    print ('Table has been created.')


def term_query(key,value,table_name,index_name):
    query = TermQuery(key, value)
    search_response = client.search(
        table_name, index_name , 
        SearchQuery(query, limit=100, get_total_count=True), 
        ColumnsToGet(return_type=ColumnReturnType.ALL)
    )
    return search_response


def range_query(columns_to_get,start_primary_key,end_primary_key,table_name,index_name):
    query = RangeQuery(columns_to_get,start_primary_key, end_primary_key)
    search_response = client.search(
        table_name, index_name , 
        SearchQuery(query, limit=100, get_total_count=True), 
        ColumnsToGet(return_type=ColumnReturnType.ALL)
    )
    return search_response


def bool_query(table_name,index_name):
    query = BoolQuery(
        must_queries=[
            RangeQuery('pct_chg', range_from=9.9, include_lower=False),
            TermQuery('_date', '20220613')
    ])
    search_response = client.search(
        table_name, index_name, 
        SearchQuery(query, limit=2, get_total_count=True), 
        ColumnsToGet(return_type=ColumnReturnType.ALL)
    )
    return search_response
# query1 = RangeQuery('beta', range_from=0.3, include_lower=False),
# query2 = TermQuery('code', '000002')
# must_queries = [query1,query2]

# res = bool_query('trading','trading_index')
# print(res)
# for key,value in res.rows:
#     print(key,value)
# response = range_query('beta',0.3,0.4,'test','query_key')
# for key,value in response.rows:
#     print(key,value)
#     print(1234)
    # print(type(value))
    # l,m,r = zip(*value)
    # print(l)
    # print(r)
    # print(m)
    # rusult = dict(zip(l,m))
    # print(rusult)
def update_row(table_name,primary_key,columns_to_update):
    # primary_key = [('gid',1), ('uid',"101")]
    update_of_attribute_columns = {
        'PUT' : columns_to_update
        # 'DELETE' : [('address', None, 1488436949003)],
        # 'DELETE_ALL' : [('mobile'), ('age')],
        # 'INCREMENT' : [('counter', -1)]
    }
    row = Row(primary_key, update_of_attribute_columns)
    condition = Condition(RowExistenceExpectation.IGNORE) # update row only when this row is exist
    consumed, return_row = client.update_row(table_name, row, condition)
    print ('Update succeed, consume %s write cu.' % consumed.write)

def delete_row(table_name,primary_key):
    row = Row(primary_key)
    condition = Condition(RowExistenceExpectation.IGNORE)
    # condition = Condition(RowExistenceExpectation.IGNORE, SingleColumnCondition("age", 25, ComparatorType.LESS_THAN))
    consumed, return_row = client.delete_row(table_name, row, condition)
    print ('Delete succeed, consume %s write cu.' % consumed.write)

def put_row(table_name,primary_key,attribute_columns):
    print(table_name)
    print(attribute_columns)
    print(primary_key)
    row = Row(primary_key, attribute_columns)
    print(row)
    # condition = Condition(RowExistenceExpectation.EXPECT_NOT_EXIST) # Expect not exist: put it into table only when this row is not exist.
    
    try:
        client.put_row(table_name, row)
    except  Exception as e:
        print(e)
    # print (u'Write succeed, consume %s write cu.' % consumed.write)

def get_row(table_name,primary_key,columns_to_get):
    consumed, return_row, next_token = client.get_row(table_name, primary_key, columns_to_get)
    # print ('Read succeed, consume %s read cu.' % consumed.read)
    # print ('Value of primary key: %s' % return_row.primary_key)
    # print ('Value of attribute: %s' % return_row.attribute_columns)
    return(return_row)

# stock = get_row('stock',[('code','000416')],['totalCash'])
# print(stock)


# 批量写入数据的上限是一次200行。
def batch_write_row(table_name,put_row_items):
    # batch put 10 rows and update 10 rows on exist table, delete 10 rows on a not-exist table.
    n = 195 # 每次上传195行
    for i in range(0, len(put_row_items), n):
        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items[i:i+n]))
        result = client.batch_write_row(request)

        # succ, fail = result.get_put()
        # for item in succ:
        #     print ('Put succeed, consume %s write cu.' % item.consumed.write)
        # for item in fail:
        #     print ('Put failed, error code: %s, error message: %s' % (item.error_code, item.error_message))

    # print ('check first table\'s update results:')
    # succ, fail = result.get_update()
    # for item in succ:
    #     print ('Update succeed, consume %s write cu.' % item.consumed.write)
    # for item in fail:
    #     print ('Update failed, error code: %s, error message: %s' % (item.error_code, item.error_message))

    # print ('check second table\'s delete results:')
    # succ, fail = result.get_delete()
    # for item in succ:
    #     print ('Delete succeed, consume %s write cu.' % item.consumed.write)
    # for item in fail:
    #     print ('Delete failed, error code: %s, error message: %s' % (item.error_code, item.error_message))

def batch_get_row(client):
    # try to get rows from two different tables
    columns_to_get = ['name', 'mobile', 'address', 'age']
    rows_to_get = []
    for i in range(0, 10):
        primary_key = [('gid',i), ('uid',i+1)]
        rows_to_get.append(primary_key)

    cond = CompositeColumnCondition(LogicalOperator.AND)
    cond.add_sub_condition(SingleColumnCondition("name", "John", ComparatorType.EQUAL))
    cond.add_sub_condition(SingleColumnCondition("address", 'China', ComparatorType.EQUAL))

    request = BatchGetRowRequest()
    request.add(TableInBatchGetRowItem(table_name_1, rows_to_get, columns_to_get, cond, 1))
    request.add(TableInBatchGetRowItem(table_name_2, rows_to_get, columns_to_get, cond, 1))
    result = client.batch_get_row(request)
    print ('Result status: %s'%(result.is_all_succeed()))

# 准备批量上传的文件
def prepare_batch_write_data(stock):
    put_row_items = []
    for index, row in stock.iterrows():
        primary_key = [['code',sf.remove_suffix(row.loc['ts_code'])], ['_date',row.loc['trade_date']]]
        k = tuple(row.to_dict())
        v= tuple(row.to_dict().values())
        attribute_columns = list(zip(tuple(row.to_dict()),row.to_dict().values()))
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        item = PutRowItem(row,condition)
        put_row_items.append(item)
    batch_write_row('trading',put_row_items)


def prepare_data(stock):
    for index, row in stock.iterrows():
        try :
            primary_key = [['code',sf.remove_suffix(row.loc['ts_code'])], ['_date',row.loc['trade_date']]]
            k = tuple(row.to_dict())
            v= tuple(row.to_dict().values())
            attribute_columns = list(zip(tuple(row.to_dict()),row.to_dict().values()))
            put_row('trading',primary_key,attribute_columns)
        except Exception as e:
            print(e)


