from gluon.tools import Service
import json
import check
import requests
import constant as CONSTANT
import datetime
from db import PGManager
import time
from wrapper import key_generation as KEY_GENERATION
from wrapper import encryption as ENCRYPTION
import transaction as TRANSACTION
import copy
import api_methods

# BASE_URL = 'http://localhost:8888'
# BASE_URL = 'http://http://116.62.226.231:8888'

service = Service()

def call():
    session.forget()
    return service()



# 1. inquire the link balance by id
# in this api service, we only supply one field request in the api /accounts/{id}
@service.run
def balance(LinkAddress):
    '''

    :param id:
    :return: a json object, e.g:
    result={
    id:'GDJHGNGELXCNMIW6PRGP4E5VDG22TCVRCJ45U4X2VD6SYNJ57EJEZXY5'
    link:123.22
    }
    '''
    Code=0
    Message='Unsuccessful'
    Result={'LinkAmount':0}

    response = {
        'Code': Code,
        'Message': Message,
        'Result': Result
    }

    try:
        constant=CONSTANT.Constant('public')
        balance=api_methods.get_balance(LinkAddress,constant)
        Code=1
        Message='Successful'
        Result=Result={'LinkAmount':balance}
    except Exception as e:
        Message=e.message
    finally:
        response={
            'Code':Code,
            'Message':Message,
            'Result':Result
        }
    return json.dumps(response)

# 2. inquire transactions by id
@service.run
def transactions(LinkAddress, limit=50, page=1, asset_code='LINK', asset_issuer=''):
    '''
    :param LinkAddress:
    :return: a json object, e.g:
    result={
    LinkAddress:'GDJHGNGELXCNMIW6PRGP4E5VDG22TCVRCJ45U4X2VD6SYNJ57EJEZXY5'
    transactions:[]
    '''

    Code = 0
    Message = 'Unsuccessful'
    Result = None
    response = {
        'Code': Code,
        'Message': Message,
        'Result': Result
    }

    constant=CONSTANT.Constant('public')
    # BASE_URL=constant.BASE_URL
    asset_issuer=constant.ISSUER_ADDRESS

    try:
        id=str(LinkAddress)
        limit=int(limit)
        page=int(page)

    except Exception as e:
        Message=e
        response['Message']=Message
        return json.dumps(response)
    if limit>100:
        Message = 'limit is too large'
        response['Message'] = Message
        return json.dumps(response)

    validity=check.check_validity_of_address(id)
    if validity==False:
        Message = 'LinkAddress is invalid'
        response['Message'] = Message
        return json.dumps(response)
    else:
        if LinkAddress==asset_issuer:
            result = {
                'LinkAddress': LinkAddress,
                'transactions': []
            }
            result['transactions'] = []
            response['Result'] = result
            response['Code'] = 1
            response['Message'] = 'Successful'
        else:

            result = {
                'LinkAddress': LinkAddress,
                'transactions': []
            }

            # inquire api_server and reformat the response
            my_psycopg = PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
            t0=time.time()
            # sql='select * from history_transactions inner join history_operations on \
            # history_transactions.id= history_operations.transaction_id where \
            #                            history_transactions.account=\'' + id +'\' and history_operations.details::text like \'%' + asset_code + '%\'  \
            #                            and history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\'  \
            #                            order by history_transactions.created_at ASC limit ' + str(limit) + ' offset ' + str(limit*(page-1))

            sql0='select id from history_accounts where address=\'' + LinkAddress + '\''
            sql1='select history_operation_id from history_operation_participants where history_account_id=(%s)' % (sql0,)
            sql2='select details::text,transaction_id from history_operations as BBB  \
                  where id in (%s) \
                  and details::text like \'%%from%%\' \
                  order by transaction_id DESC limit %d offset %d' % (sql1,limit,limit*(page-1))
            result_of_details=my_psycopg.select(sql2)
            '''
            select id, created_at from history_transactions as AAA where id in 
            (select transaction_id from history_operations as C where id in (select history_operation_id from history_operation_participants as A 
            where history_account_id=231))
            and id in (select transaction_id from history_operations as BBB where id in (select history_operation_id from history_operation_participants where history_account_id=231)
            and details::text like '%from%')
            order by created_at DESC
            '''
            if len(result_of_details)==0:
                response['Result'] = result
                response['Code'] = 1
                response['Message'] = 'Out of index error'
            else:
                transaction_ids=[]
                for detail in result_of_details:
                    transaction_ids.append(str(detail[1]))
                if len(transaction_ids)==1:
                    tmp0=' id=' + transaction_ids[0]
                else:
                    transaction_ids = ','.join(transaction_ids)
                    tmp0=' id in (' + transaction_ids + ')'
                sql3='select id, created_at from history_transactions where %s order by id' % (tmp0,)
                result_of_transactions = my_psycopg.select(sql3)
                transactions=[]
                for i in range(len(result_of_details)):
                    detail=json.loads(result_of_details[i][0])
                    transaction=copy.deepcopy(detail)
                    transaction['id']=str(result_of_details[i][1])
                    for tt in result_of_transactions:
                        if result_of_details[i][1]==tt[0]:
                            transaction['time']=(tt[1]+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                    transactions.append(transaction)
                    if transaction['from']==id:
                        transaction['amount']='-'+transaction['amount']
                    else:
                        transaction['amount'] = '+' + transaction['amount']
                result['transactions']=transactions
                response['Result']=result
                response['Code']=1
                response['Message']='Successful'
                t=time.time()-t0
    return json.dumps(response)

# √√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√
# 3. post transaction details:
@service.run
def orders(OrderNo, UserToken, OrderAmount):
    '''
    url='http://localhost:8000/link/api/call/run/orders'
    data='{"orderno": "123", "usertoken": "ffff", "orderamount": 1234}'

    :param OrderNo:
    :param UserToken:
    :param OrderAmount:
    :return:
    '''
    response={
        'Code':'',
        'Message':'',
        'Result':''
    }
    Code=0
    Message=None
    Result=None
    try:
        OrderAmount=float(OrderAmount)
        if OrderAmount<0.000001 or OrderAmount>100:
            Message='Order amount must be in the range:0.000001-100'
            response = {
                'Code': Code,
                'Message': Message,
                'Result': Result
            }
            return json.dumps(response)
    except:
        Message='Order amount is not a valid number'
        response = {
            'Code': Code,
            'Message': Message,
            'Result': Result
        }
        return json.dumps(response)
    try:
        constant=CONSTANT.Constant('public')
        my_psycopg = PGManager(**constant.DB_CONNECT_ARGS)
        timestamp=int(time.time())
        sql='insert into orders(orderno, usertoken,orderamount,created_at,is_filled) values(\'' + str(OrderNo) +'\',\'' + str(UserToken) + '\',' + str(OrderAmount) + ',' + str(timestamp) + ',0)'
        my_psycopg.execute(sql)
        # inquire usertoken in table private_keys, if not exists, insert a record
        sql = 'select * from private_keys where user_token=\'' + UserToken + '\''
        rows=my_psycopg.select(sql)
        if len(rows)==0:
            keypair = KEY_GENERATION.generate_keypairs(1, constant.AES_KEY, constant.AES_IV, False)[0]
            sql = 'insert into private_keys(user_token,private_key,public_key,is_activated) values(\'%s\',\'%s\',\'%s\',0)' % (UserToken, keypair[0], keypair[1])
            my_psycopg.execute(sql)

            # from wrapper import client as CLIENT
            # client=CLIENT.Client(private_key=constant.SEED,api_server=constant.API_SERVER)
            # client.fund(keypair[1],100)
        else:
            keypair = (rows[0][2],rows[0][3])

        # private_key=ENCRYPTION.decrypt(keypair[0])
        Result={
            'UserToken':UserToken,
            'LinkPrivateKey':keypair[0],
            'LinkAddress':keypair[1]
        }
        Code = 1
        Message = 'Successful'

    except Exception as e:
        Code=0
        Message=e
    response={
        'Code': Code,
        'Message': Message,
        'Result': Result
    }
    return json.dumps(response)


# 4. get all info of an account:
# def info(address):
#     response={
#         'Address':'',
#         'Message':'',
#         'Result':''
#     }
#     Code=0
#     Message=None
#     Result={
#         'Address':'',
#         'LinkBalance':0,
#         'TransactionCount':0,
#         'TotalSpent':0,
#         'TotalReceived':0,
#         'Transactions':[]
#     }
#
#
#     try:
#         constant=CONSTANT.Constant('test')
#         BASE_URL=constant.BASE_URL
#
#         # initialization:
#         asset_issuer = constant.ISSUER_ADDRESS
#
#         validity=check.check_validity_of_address(address)
#         if validity==False:
#             Code=0
#             Message='Account is invalid'
#         else:
#             # inquire api_server and reformat the response
#             _response=json.loads(requests.get(BASE_URL+'/accounts/'+address).text)
#             id=_response.get('id','None')
#             if id=='None':
#                 Code=0
#                 Message='Account does not exist'
#             else:
#                 # 1. get the link balance
#                 Code=1
#                 Message='Successful'
#                 LinkBalance=0
#                 balances=_response.get('balances',[])
#                 for item in balances:
#                     item=dict(item)
#                     if item.get('asset_code','') == 'LINK' and item.get('asset_issuer','') == constant.ISSUER_ADDRESS:
#                         LinkBalance=float(item['balance'])
#
#                 # 2. get the total received and total spent
#                 # my_psycopg = PsycoPG('horizon', 'cc5985', 'Caichong416', '116.62.226.231', '5432')
#                 # t0 = time.time()
#                 # sql = 'select * from history_operations where \
#                 #        history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\' and \
#                 #        history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\' and \
#                 #                                    order by history_transactions.created_at ASC limit ' + str(
#                 #     limit) + ' offset ' + str(limit * (page - 1))
#                 rows = my_psycopg.select(sql)
#                 t = time.time() - t0
#     except Exception as e:
#         Code=0
#         Message=e
#     finally:
#         response={
#             'Code':Code,
#             'Message':Message,
#             'Result':Result
#         }
#     return json.dumps(response)










@service.run
def create_table(sql=''):
    '''
    sql='create table orders(id SERIAL primary key ,UserToken varchar(32) not null,OrderNo varchar(32) not null,OrderAmount decimal not null , created_at bigint not null, is_filled int )'
    sql = 'create table private_keys(id SERIAL primary key ,user_token varchar(40),private_key varchar(128) not null,public_key varchar(128) not null , starting_balance decimal , starting_time timestamp default current_timestamp, is_activated int default 0, has_trusted int default 0 )'
    :param sql:
    :return:
    '''
    constant=CONSTANT.Constant('test')
    my_psycopg = PGManager(**constant.DB_CONNECT_ARGS)
    # my_psycopg = PsycoPG('lyl_orders', 'cc5985', 'Caichong416', 'localhost', '5432')
    result=my_psycopg.create_table(sql)
    return json.dumps(result)

@service.run
def truncate_tables(table_names=None):
    '''

    :param table_name:
    :return:
    '''

    try:
        constant=CONSTANT.Constant('test')
        my_psycopg = PGManager(**constant.DB_CONNECT_ARGS)
        if table_names==None:
            table_names=['orders','private_keys']
        for table_name in table_names:
            result = my_psycopg.execute('truncate table ' + table_name)
        result={'Message':'OK'}
    except Exception as e:
        result={'Message':e}
    return json.dumps(result)