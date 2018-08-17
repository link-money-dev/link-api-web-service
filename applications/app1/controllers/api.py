from gluon.tools import Service
import json
import check
import requests
import constant as CONSTANT
import datetime
from psql import PsycoPG
import time

# BASE_URL = 'http://localhost:8888'
# BASE_URL = 'http://http://116.62.226.231:8888'

service = Service()


def call():
    session.forget()
    return service()


@service.run
def add(x,y):
    x=int(x)
    y=int(y)
    result={'result':x+y}
    return json.dumps(result)

@service.run
def charge():
    print('#20')
    args=request.post_vars
    args=json.loads(args)
    return args

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
    response={
        'Code':'',
        'Message':'',
        'Result':''
    }
    Code=0
    Message=None
    Result={'LinkAmount':0}

    try:
        constant=CONSTANT.Constant('test')
        BASE_URL=constant.BASE_URL

        validity=check.check_validity_of_address(LinkAddress)
        if validity==False:
            Code=0
            Message='Account is invalid'
            Result={'LinkAmount':0}
        else:
            # inquire api_server and reformat the response
            _response=json.loads(requests.get(BASE_URL+'/accounts/'+LinkAddress).text)
            id=_response.get('id','None')
            if id=='None':
                Code=0
                Message='Account does not exist'
                Result={'LinkAmount':0}
            else:
                Code=1
                Message='Successful'
                Result={'LinkAmount':0}
                balances=_response.get('balances',[])
                for item in balances:
                    item=dict(item)
                    if item.get('asset_code','') == 'LINK' and item.get('asset_issuer','') == constant.ISSUER_ADDRESS:
                        Result['LinkAmount']=float(item['balance'])

    except Exception as e:
        Code=0
        Message=e
        Result={'LinkAmount':0}
    finally:
        response={
            'Code':Code,
            'Message':Message,
            'Result':Result
        }
    return json.dumps(response)

# 2. inquire transactions by id
@service.run
def transactions(id, limit=50, page=1, asset_code='LINK', asset_issuer=''):
    '''
    :param id:
    :return: a json object, e.g:
    result={
    id:'GDJHGNGELXCNMIW6PRGP4E5VDG22TCVRCJ45U4X2VD6SYNJ57EJEZXY5'
    transactions:[
        {

        },
        {}
        {}...
        ]
    }
    '''
    constant=CONSTANT.Constant('test')
    BASE_URL=constant.BASE_URL
    asset_issuer=constant.ISSUER_ADDRESS

    try:
        id=str(id)
        limit=int(limit)
        page=int(page)

    except Exception as e:
        return json.dumps(e)
    if limit>100:
        return json.dumps({'warning':'limit should be less than 100'})
    result={
        'id':None,
        'transactions':[]
    }
    validity=check.check_validity_of_address(id)
    if validity==False:
        return json.dumps(({'error':'id is invalid'}))
    else:
        # inquire api_server and reformat the response
        my_psycopg = PsycoPG('horizon_testnet', 'cc5985', 'caichong', 'localhost', '5432')
        my_psycopg = PsycoPG('horizon','cc5985','Caichong416','116.62.226.231','5432')
        t0=time.time()
        sql='select * from history_transactions inner join history_operations on \
                                  history_transactions.id= history_operations.transaction_id where \
                                   history_transactions.account=\'' + id +'\' and history_operations.details::text like \'%' + asset_code + '%\'  \
                                   and history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\'  \
                                   order by history_transactions.created_at ASC limit ' + str(limit) + ' offset ' + str(limit*(page-1))
        rows = my_psycopg.select(sql)
        t=time.time()-t0
        result['id']=id
        cnt=0
        for record in rows:
            if cnt>=100:
                break

            transaction_hash=record[0]
            ledger=record[1]
            created_at=record[7].strftime('%Y-%m-%dT%H:%M:%S')
            memo_type=None if record[15]=='none' else record[15]
            memo=record[16]
            transaction_id=record[18]
            details=dict(record[22])
            fromer = None
            toer = None
            amount = None
            asset_code='native'
            asset_issuer='Fotono'
            if details.has_key('asset_code') and details.has_key('from') and details.has_key('to'):
                fromer=details['from']
                toer=details['to']
                amount=details['amount']
                try:
                    asset_code=details['asset_code']
                except:
                    a=1
                asset_issuer=details['asset_issuer']
            elif details.has_key('funder'):
                fromer=details['funder']
                toer=details['account']
                amount=details['starting_balance']

            if asset_code=='LINK' and asset_issuer==constant.ISSUER_ADDRESS:
                transaction = {
                    'transaction_id': transaction_id,
                    'ledger': ledger,
                    'created_at': created_at,
                    'memo_type': memo_type,
                    'memo': memo,
                    'transaction_hash': transaction_hash,
                    'asset_code': asset_code,
                    'asset_issuer': asset_issuer,
                    'from': fromer,
                    'to': toer,
                    'amount': amount
                }
                result['transactions'].append(transaction)
                cnt += 1
            else:
                # To be implemented...
                pass

    return json.dumps(result)

# 3. post transaction details:
@service.run
def orders(OrderNo, UserToken, OrderAmount):
    my_psycopg = PsycoPG('test', 'cc5985', 'caichong', 'localhost', '5432')
    timestamp=time.time()
    sql='insert into orders(usertoken,orderno,orderamount,created_at) values(\'' + str(UserToken) + '\',\'' + str(OrderNo) + '\',' + str(OrderAmount) + ',' + str(timestamp) + ')'
    my_psycopg.execute(sql)


# 4. get all info of an account:
def info(address):
    response={
        'Address':'',
        'Message':'',
        'Result':''
    }
    Code=0
    Message=None
    Result={
        'Address':'',
        'LinkBalance':0,
        'TransactionCount':0,
        'TotalSpent':0,
        'TotalReceived':0,
        'Transactions':[]
    }


    try:
        constant=CONSTANT.Constant('test')
        BASE_URL=constant.BASE_URL

        # initialization:
        asset_issuer = constant.ISSUER_ADDRESS

        validity=check.check_validity_of_address(address)
        if validity==False:
            Code=0
            Message='Account is invalid'
        else:
            # inquire api_server and reformat the response
            _response=json.loads(requests.get(BASE_URL+'/accounts/'+address).text)
            id=_response.get('id','None')
            if id=='None':
                Code=0
                Message='Account does not exist'
            else:
                # 1. get the link balance
                Code=1
                Message='Successful'
                LinkBalance=0
                balances=_response.get('balances',[])
                for item in balances:
                    item=dict(item)
                    if item.get('asset_code','') == 'LINK' and item.get('asset_issuer','') == constant.ISSUER_ADDRESS:
                        LinkBalance=float(item['balance'])

                # 2. get the total received and total spent
                # my_psycopg = PsycoPG('horizon', 'cc5985', 'Caichong416', '116.62.226.231', '5432')
                # t0 = time.time()
                # sql = 'select * from history_operations where \
                #        history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\' and \
                #        history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\' and \
                #                                    order by history_transactions.created_at ASC limit ' + str(
                #     limit) + ' offset ' + str(limit * (page - 1))
                rows = my_psycopg.select(sql)
                t = time.time() - t0
    except Exception as e:
        Code=0
        Message=e
    finally:
        response={
            'Code':Code,
            'Message':Message,
            'Result':Result
        }
    return json.dumps(response)










@service.run
def create_table(sql=''):
    '''
    sql='create table orders(id integer not null primary key,UserToken varchar(32) not null,OrderNo varchar(32) not null,OrderAmount decimal'
    :param sql:
    :return:
    '''
    my_psycopg = PsycoPG('test', 'cc5985', 'caichong', 'localhost', '5432')
    result=my_psycopg.create_table(sql)
    return json.dumps(result)
























# test for psycopg2
@service.run
def test_psycopg2(limit=50, page=1, total_limit=200):
    '''
    select top 50 * from pagetest
    where id not in (select top 9900 id from pagetest order by id)
    order by id
    :return: a dict such as
    {
        id: ...,

    }
    '''
    if limit*page > total_limit and total_limit!=0:
        return []
    from psql import PsycoPG
    my_psycopg=PsycoPG('horizon_testnet','cc5985','caichong','localhost','5432')
    # select * from history_transactions where created_at not in (select created_at from history_transactions order by created_at limit 100) order by created_at limit 50
    rows=my_psycopg.select('select * from history_transactions where created_at not in (select created_at from history_transactions order by created_at limit ' + one_page_limit*(page-1) + ') order by created_at limit ' + one_page_limit)
    a=1


