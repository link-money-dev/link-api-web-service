# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import os,sys

# 姑且算是一个夹具文件
# 2. 数据库文件的位置，默认是运行的程序的目录+文件名，只需要确认文件名即可：
path=os.getcwd()
DB_NAME=path+'\\keys.db'
TABLE_NAME='private_keys'

# 3. BASE_URL
BASE_URL_TEST='http://116.62.226.231:12346'
BASE_URL_PUBLIC='http://47.75.115.19:12346'
BASE_URL_LOCAL='http://localhost:8000'
BASE_URL=BASE_URL_TEST

# 4. DB_CONNECT_ARGS
DB_CONNECT_ARGS_TEST={'database':'lyl_orders', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}
DB_CONNECT_ARGS_PUBLIC={'database':'lyl_orders', 'user':'cc5985', 'pw':'Caichong416', 'host':'47.75.115.19', 'port':'5432'}
DB_CONNECT_ARGS_LOCAL={'database':'lyl_orders', 'user':'cc5985', 'pw':'Caichong416', 'host':'47.75.115.19', 'port':'5432'}

# 5. HORIZON_CONNECT_ARGS
DB_CONNECT_ARGS_HORIZON_TEST={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}
DB_CONNECT_ARGS_HORIZON_PUBLIC={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'47.75.115.19', 'port':'5432'}
DB_CONNECT_ARGS_HORIZON_LOCAL={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}

# 6. HORIZON_BASE_URL
HORIZON_BASE_URL_TEST='http://116.62.226.231:8888'
HORIZON_BASE_URL_PUBLIC='http://47.75.115.19:8888'
HORIZON_BASE_URL_LOCAL='http://localhost:8888'
HORIZON_BASE_URL=BASE_URL_TEST

# DB_HORIZON_TEST={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}
# DB_HORIZON_PUBLIC={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}
class Constant():

    # define a method, which is used to choose a server:
    # 1. main net:
    def __init__(self, server='local'):
        if server=='local':
            self.SEED = 'SDSSWWPCGGRDB6SVVOJUWFQ3ODQFX62GVTKCPELNULO5PXVCFE67L7HO'
            self.API_SERVER='local'
            self.ISSUER_ADDRESS='GDJHGNGELXCNMIW6PRGP4E5VDG22TCVRCJ45U4X2VD6SYNJ57EJEZXY5'
            self.DISTRIBUTOR_SEED='SCV5M6ISCCVYBQ5Y4GQ3L2A6JM25Z4CAIZOBSWBRURFCBF4OKW3OAM3M'
            self.DISTRIBUTOR_ADDRESS='GCHZDZXYLZ76XADS7735LK3OJUFZ2TBSXAR23YXKXCXXHUEEVT5C37PY'
            self.BASE_URL='http://localhost:8888'


        elif server == 'public':
            self.SEED = 'SDYYLWVFTUPF6QKVYEUWP7GR5X3SFY2MOPMEPPPCES5ZT2DYJIBY4P63'
            self.API_SERVER = 'public'
            self.ISSUER_ADDRESS = 'GBGP4NT7S52HTW6EZI3RM3YKAAHEBQNBMMPQALNUJWUURQPX5AKCG3CI'
            self.DISTRIBUTOR_SEED = 'SCV5M6ISCCVYBQ5Y4GQ3L2A6JM25Z4CAIZOBSWBRURFCBF4OKW3OAM3M'
            self.DISTRIBUTOR_ADDRESS = 'GCHZDZXYLZ76XADS7735LK3OJUFZ2TBSXAR23YXKXCXXHUEEVT5C37PY'
            self.FOTONO_STARTING_BALANCE = 100
            self.BASE_URL = BASE_URL_PUBLIC
            self.HORIZON_DB_CONNECT_ARGS = DB_CONNECT_ARGS_HORIZON_PUBLIC
            self.DB_CONNECT_ARGS = DB_CONNECT_ARGS_PUBLIC
            self.HORIZON_BASE_URL = HORIZON_BASE_URL_PUBLIC
            self.AES_KEY = 'Xjr;H^P(RepxganS'
            self.AES_IV = '7297115918661978'

        elif server=='stellar':
            self.SEED='SDIUGGIWZ5GHG5RXPDPANBMXEW5B3VDIAY4SSFTWQ42CLBBK2YOU5FYS'
            self.API_SERVER = 'stellar'


        else:
            self.SEED = 'SBRYFNS7O4RPXZR3VRZAIXQJNISHSJQHBG5SXDTU6LP2V7SMDRL4ZPT4'
            self.API_SERVER = 'test'
            self.ISSUER_ADDRESS = 'GBGP4NT7S52HTW6EZI3RM3YKAAHEBQNBMMPQALNUJWUURQPX5AKCG3CI'
            self.DISTRIBUTOR_SEED = 'SCV5M6ISCCVYBQ5Y4GQ3L2A6JM25Z4CAIZOBSWBRURFCBF4OKW3OAM3M'
            self.DISTRIBUTOR_ADDRESS = 'GCHZDZXYLZ76XADS7735LK3OJUFZ2TBSXAR23YXKXCXXHUEEVT5C37PY'
            self.BASE_URL = 'http://116.62.226.231:8888'
            self.DB_CONNECT_ARGS=DB_CONNECT_ARGS_TEST
            self.DB_HORIZON=DB_HORIZON_TEST
            self.AES_KEY='Xjr;H^P(RepxganS'
            self.AES_IV='7297115918661978'


