from gluon.tools import Service
import json
import requests
import datetime
import time
import api_methods
import constant as CONSTANT
from db import PGManager

# BASE_URL = 'http://localhost:8888'
# BASE_URL = 'http://http://116.62.226.231:8888'

service = Service()

def call():
    session.forget()
    return service()

# def index():
#     response.flash = T("Hello World")
#     return dict(message=T('Welcome to web2py!'))

# 1. inquire the link balance by id
# in this api service, we only supply one field request in the api /accounts/{id}
@service.run
def see(LinkAddress):
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
        my_psycopg = PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
        # get balance:
        balance=api_methods.get_balance(LinkAddress,constant)
        # get number of transactions:
        sql0 = 'select id from history_accounts where address=\'' + LinkAddress + '\''
        sql1 = 'select history_operation_id from history_operation_participants where history_account_id=(%s)' % (sql0,)
        sql2 = 'select count(*) from history_operations as BBB  \
                          where id in (%s) \
                          and details::text like \'%%from%%\' \
                          and details::text like \'%% "asset_code": "LINK",%%\' \
                          ' % (sql1,)
        result_of_details = my_psycopg.select(sql2)
        transaction_number=result_of_details[0][0]
        # rows=my_psycopg.select('select count(*) from ')

        Code=1
        Message='Successful'
        Result={'LinkAmount':balance}








    except Exception as e:
        Message=e.message
    finally:
        response={
            'Code':Code,
            'Message':Message,
            'Result':Result
        }

    return json.dumps(response)

