import check
import requests
import json
import error
from db import PGManager

def get_balance(LinkAddress, constant):
    BASE_URL = constant.BASE_URL

    validity = check.check_validity_of_address(LinkAddress)
    if validity == False:
        raise error.APIError('Account is invalid')
    else:
        # inquire api_server and reformat the response
        _response = json.loads(requests.get(BASE_URL + '/accounts/' + LinkAddress).text)
        id = _response.get('id', 'None')
        if id == 'None':
            raise error.APIError('Account does not exist')
        else:
            link_balance=0
            balances = _response.get('balances', [])
            for item in balances:
                item = dict(item)
                if item.get('asset_code', '') == 'LINK' and item.get('asset_issuer', '') == constant.ISSUER_ADDRESS:
                    link_balance=float(item['balance'])
                    return link_balance
            return link_balance

def get_transactions(LinkAddress, constant, limit=50, page=1, asset_code='LINK' ):
    # constant = CONSTANT.Constant('test')
    BASE_URL = constant.BASE_URL
    asset_issuer = constant.ISSUER_ADDRESS

    if LinkAddress.__class__=='str':
        raise error.APIError('LinkAddress must be String type')
    if limit.__class__=='int':
        raise error.APIError('limit must be Integer type')
    if page.__class__=='int':
        raise error.APIError('page must be Integer type')
    if limit > 100:
        raise error.APIError('limit should be less than 100')
    validity = check.check_validity_of_address(LinkAddress)
    if validity == False:
        raise error.APIError('Account is invalid')
    else:

        result = {
            'LinkAddress': LinkAddress,
            'transactions': []
        }

        # inquire api_server and reformat the response
        my_psycopg = PGManager(**constant.DB_HORIZON)
        # sql='select * from history_transactions inner join history_operations on \
        # history_transactions.id= history_operations.transaction_id where \
        #                            history_transactions.account=\'' + id +'\' and history_operations.details::text like \'%' + asset_code + '%\'  \
        #                            and history_operations.details::text like \'%"asset_issuer": "' + asset_issuer + '"%\'  \
        #                            order by history_transactions.created_at ASC limit ' + str(limit) + ' offset ' + str(limit*(page-1))

        sql0 = 'select id from history_accounts where address=\'' + LinkAddress + '\''
        sql1 = 'select history_operation_id from history_operation_participants where history_account_id=(%s)' % (sql0,)
        sql2 = 'select details::text,transaction_id from history_operations as BBB  \
                  where id in (%s) \
                  and details::text like \'%%from%%\' \
                  order by transaction_id DESC limit %d offset %d' % (sql1, limit, limit * (page - 1))
        result_of_details = my_psycopg.select(sql2)
        '''
        select id, created_at from history_transactions as AAA where id in 
        (select transaction_id from history_operations as C where id in (select history_operation_id from history_operation_participants as A 
        where history_account_id=231))
        and id in (select transaction_id from history_operations as BBB where id in (select history_operation_id from history_operation_participants where history_account_id=231)
        and details::text like '%from%')
        order by created_at DESC
        '''
        if len(result_of_details) == 0:
            raise error.APIError('Out of index error')
        else:
            transaction_ids = []
            for detail in result_of_details:
                transaction_ids.append(str(detail[1]))
            if len(transaction_ids) == 1:
                tmp0 = ' id=' + transaction_ids[0]
            else:
                transaction_ids = ','.join(transaction_ids)
                tmp0 = ' id in (' + transaction_ids + ')'
            sql3 = 'select id, created_at from history_transactions where %s order by id' % (tmp0,)
            result_of_transactions = my_psycopg.select(sql3)
            transactions = []
            for i in range(len(result_of_details)):
                detail = json.loads(result_of_details[i][0])
                transaction = copy.deepcopy(detail)
                transaction['id'] = str(result_of_details[i][1])
                for tt in result_of_transactions:
                    if result_of_details[i][1] == tt[0]:
                        transaction['time'] = tt[1].strftime("%Y-%m-%d %H:%M:%S")
                transactions.append(transaction)
                if transaction['from'] == id:
                    transaction['amount'] = '-' + transaction['amount']
                else:
                    transaction['amount'] = '+' + transaction['amount']
            result['transactions'] = transactions
            response['Result'] = result
            response['Code'] = 1
            response['Message'] = 'Successful'
            t = time.time() - t0
