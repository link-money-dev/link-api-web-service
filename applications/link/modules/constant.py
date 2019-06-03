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
BASE_URL_PUBLIC='http://47.52.0.154:12346'
BASE_URL_LOCAL='http://localhost:8000'
BASE_URL=BASE_URL_TEST

# 4. DB_CONNECT_ARGS
DB_CONNECT_ARGS_TEST={'database':'lyl_orders', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}
DB_CONNECT_ARGS_PUBLIC={'database':'lyl_orders', 'user':'cc5985', 'pw':'Caichong416', 'host':'47.52.0.154', 'port':'5432'}
DB_CONNECT_ARGS_LOCAL={'database':'lyl_orders', 'user':'cc5985', 'pw':'Caichong416', 'host':'localhost', 'port':'5432'}

# 5. HORIZON_CONNECT_ARGS
DB_CONNECT_ARGS_HORIZON_TEST={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}
DB_CONNECT_ARGS_HORIZON_PUBLIC={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'47.52.0.154', 'port':'5432'}
DB_CONNECT_ARGS_HORIZON_LOCAL={'database':'horizon', 'user':'cc5985', 'pw':'Caichong416', 'host':'116.62.226.231', 'port':'5432'}

# 6. HORIZON_BASE_URL
HORIZON_BASE_URL_TEST='http://116.62.226.231:8888'
HORIZON_BASE_URL_PUBLIC='http://47.52.0.154:8888'
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

            self.ENCRYPTED_MASTER_SEED = '7cf51b0a17b1b4f65bedf437654a65272a95eacf0dc93d994d8244b579a529a54d4c7608a96f30f22baf9f227feaec9c18895ce75f8c760018eda9affffcfabf'
            self.SEED = 'SDCCOAL6ILCJXWQPDZLRNHTMAHLZHC2IIHGPSQMLSIPHRTLNCFNT4A66'
            self.API_SERVER = 'public'
            self.ISSUER_ADDRESS = 'GCA3SBI2Y6AYHLAW2GBTS7C5HTSFW6OTZACHOVJGBQ6JENTE3ZXPNNSL'
            self.DISTRIBUTOR_SEED = 'SCWDXYXEJL6GQWXUADDGFGFPF64ORWHXA7R2FNV4UVS6VIBIQCVD53JH'
            self.DISTRIBUTOR_ADDRESS = 'GCONR7JZN7VUSFI54BS76VQJRWGUZDLQFPTB7DXHNP6E5KZECUW77VFL'
            self.FOTONO_STARTING_BALANCE = 100
            self.BASE_URL = BASE_URL_PUBLIC
            self.HORIZON_DB_CONNECT_ARGS = DB_CONNECT_ARGS_HORIZON_PUBLIC
            self.DB_CONNECT_ARGS = DB_CONNECT_ARGS_PUBLIC
            self.HORIZON_BASE_URL = HORIZON_BASE_URL_PUBLIC
            self.ASSET_CODE = 'LINK'
            self.AES_KEY=''
            self.AES_IV=''

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


