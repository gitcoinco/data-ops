import pandas as pd 
from pandas.io.json import json_normalize
pd.options.mode.chained_assignment = None
import os, requests, json
import gdax


def get_minted_kudos(data, coin_data):
    """
    Formats minted kudos data.
    @input: raw transaction data, raw coin data
    @output: formatted minted kudos data
    """
    # get minted kudos data
    df = json_normalize(data['result'])
    df.loc[:, 'eth_value'] = df['value'].astype('int64') / 1000000000000000000
    # timestamp to date
    minted_kudos_txns = df[df['eth_value'] == 0.4]
    minted_kudos_txns.loc[:, 'timeStamp'] = pd.to_datetime(minted_kudos_txns['timeStamp'], unit='s').dt.date
    # coin conversions
    final = pd.merge(minted_kudos_txns, coin_data, how='left', left_on='timeStamp', right_on='_timestamp')
    # add year and month and week
    final.loc[:, 'month'] = pd.to_datetime(final['_timestamp']).dt.to_period('M')
    final.loc[:, 'week'] = pd.to_datetime(final['_timestamp']).dt.to_period('W').apply(lambda x: x.start_time)
    # revenue calculations
    final.loc[:, 'usd_amount'] = final['eth_value'] * final['close'] 
    return final


def get_coin_data(public_client):
    """
    Gets ether prices.
    @input: gdax public client
    @output: ether price data
    """
    # only for the past 300 days, additional work here after fee release + 300 days
    eth_data = public_client.get_product_historic_rates('ETH-USD', granularity=60*60*24)
    eth_data = pd.DataFrame(eth_data)
    eth_data.columns = ['_timestamp', 'low', 'high', 'open', 'close', 'volume']
    eth_data.loc[:, '_timestamp'] = eth_data['_timestamp'].astype(float)
    eth_data.loc[:, '_timestamp'] = pd.to_datetime(eth_data['_timestamp'], unit='s').dt.date
    return eth_data


def get_transactions(address, key):
    """
    Gets raw transaction data.
    @input: etherscan key and address
    @output: raw transaction data for that address
    """
    # get normal transactions by address
    url = 'http://api.etherscan.io/api?module=account&action=txlist&address=' + address + '&startblock=0&endblock=99999999&sort=asc&apikey=' + key
    # get raw data
    r = requests.get(url)
    r.status_code
    return r.json()


def initialize_gdax():
    """
    Initializes GDAX public and auth clients.
    @input: none
    @output: public and private clients
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.creds')
    with open(os.path.join(credential_dir, 'gdax_api_creds.json')) as f:
        creds = json.load(f)
    key = creds['key']
    secret = creds['secret']
    passphrase = creds['passphrase']
    # gdax public client will soon be deprecated
    public_client = gdax.PublicClient()
    auth_client = gdax.AuthenticatedClient(key, secret, passphrase)
    request = auth_client.get_fills(limit=100)
    return public_client, auth_client


def initialize_etherscan():
    """
    Initializes Etherscan creds.
    @input: none
    @output: keys and address
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.creds')
    with open(os.path.join(credential_dir, 'etherscan_creds.json')) as f:
        config = json.load(f)
    key = config['key']
    address = config['address']
    return address, key


if __name__ == '__main__':
    # initialize apis
    address, key = initialize_etherscan()
    public_client, auth_client = initialize_gdax()
    # get data
    data = get_transactions(address, key)
    coin_data = get_coin_data(public_client)
    # get final result
    result = get_minted_kudos(data, coin_data)
    # print final result
    print 'total minted kudos revenue: ${0}'.format(round(result['usd_amount'].sum(), 2))
    print 'minted kudos revenue by week: \n{0}'.format(result.groupby('week').agg({'usd_amount': 'sum'}).reset_index(0))
    print 'minted kudos revenue by month: \n{0}'.format(result.groupby('month').agg({'usd_amount': 'sum'}).reset_index(0))

