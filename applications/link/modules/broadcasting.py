import requests
import json
import time

def get_all_payments(account_id, interval=3600):
    this_url = ''
    now=time.time()
    # account_id = 'GCNY2H4OAQNSVG2WUQ5EGABFLEG2GXF3OZZVJCQB7N2KCIGWVTY6WTHB'
    base_url = 'http://47.75.115.19:8888/accounts/' + account_id + '/payments/'
    base_url = base_url + '?limit=10&order=desc'

    records = []
    records_from_requests=None
    this_url = base_url

    exit_flag=False
    while records_from_requests != []:
        res = requests.get(this_url)
        records_from_requests = json.loads(res.text)['_embedded']['records']
        for record in records_from_requests:
            t=int(time.mktime(time.strptime(record['created_at'], '%Y-%m-%dT%H:%M:%SZ')))+3600*8
            if t>now-interval:
                records.append(record)
            else:
                exit_flag=True
                break
        if exit_flag==True:
            break
        this_url = json.loads(res.text)['_links']['next']['href']

    return records


def find_max_coin_sender(records):
    senders = {}
    for record in records:
        asset_issuer = record.get('asset_issuer', 'fotono.org')
        asset_code = record.get('asset_code', 'ftn')
        if asset_code == 'CNY' and asset_issuer == 'GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD':
            sender = record['from']
            if senders.__contains__(sender):
                senders[sender] += float(record['amount'])
            else:
                senders[sender] = float(record['amount'])

    max_coin_sender = None
    max_coin_sent = 0
    for sender in senders.keys():
        if senders[sender] > max_coin_sent:
            max_coin_sent = senders[sender]
            max_coin_sender = sender
    return max_coin_sender

def get_all_payments_of_a_sender(sender,records):
    all_payments = []
    for record in records:
        asset_code = record.get('asset_code', 'ftn')
        asset_issuer = record.get('asset_issuer', 'fotono.org')
        if asset_code == 'CNY' and asset_issuer == 'GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD':
            if record['from'] == sender:
                all_payments.append(record)
    return all_payments

def get_all_memos_from_payments(payments):
    all_memos = []

    for payment in payments:
        this_url = payment['_links']['transaction']['href']
        res = requests.get(this_url).text
        res = json.loads(res)
        memo = res.get('memo', '')
        all_memos.append(memo)
    return all_memos

def filter_memos(memos):
    result=[]
    for memo in memos:
        memo=str(memo)
        if memo[2]=='>' and memo[:2].isdigit():
            result.append(memo)
    return result

def concatenate_memos(memos):
    result=''
    memos.sort()
    for memo in memos:
        result+=memo[3:]
    return result