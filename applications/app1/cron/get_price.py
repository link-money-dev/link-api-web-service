import requests
import time
import json

ISSUER='GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC'
BASE_URL='http://47.75.115.19:8888'
QUERY_URL="/trade_aggregations"

params = [
    {
        'base_asset_code': "CNY",
        'base_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
        'counter_asset_code': 'LINK',
        'counter_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
    },
    {
        'base_asset_code': "CNY",
        'base_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
        'counter_asset_code': 'CNY',
        'counter_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
    },
    {
        'base_asset_code': "CNY",
        'base_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
        'counter_asset_code': 'FTN',
        'counter_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
    },
    {
        'base_asset_code': "CNY",
        'base_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
        'counter_asset_code': 'FTN',
        'counter_asset_issuer': 'fotono.info',
    },
    {
        'base_asset_code': "CNY",
        'base_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
        'counter_asset_code': 'USD',
        'counter_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
    },
    {
        'base_asset_code': "CNY",
        'base_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
        'counter_asset_code': 'BTC',
        'counter_asset_issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
    },
]

# get price from horizon:
def get_prices_from_horizon():
    prices = []
    for param in params:
        query_string = "base_asset_type=credit_alphanum4&base_asset_code={0}&base_asset_issuer={1}&counter_asset_type=credit_alphanum4&counter_asset_code={2}&counter_asset_issuer={3}&start_time=0&end_time={4}&resolution=86400000".format(
            param['base_asset_code'], param['base_asset_issuer'], param['counter_asset_code'],
            param['counter_asset_issuer'], str(int(time.time()*1000)))
        url = BASE_URL + QUERY_URL + '?' + query_string
        data=json.loads(requests.get(url).content)
        price = {
                    'price': data['_embedded']['records'][0]['close_r']['D'],
                    'code': param['counter_asset_code'],
                    'issuer': 'GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC',
                    'home_domain': 'fotono.info'
                }
        prices.append(price)
    prices=json.dumps(prices)
    return prices

# "base_asset_type=credit_alphanum4&base_asset_code=LINK&base_asset_issuer=GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC&counter_asset_type=credit_alphanum4&counter_asset_code=CNY&counter_asset_issuer=GBW4VQWWSKIYUJMXUQBF6DLLA6LZUGXN3S4ZR22EX6VFNMZIYDRENAHC&start_time=0&end_time=1532104051392&resolution=86400000"
