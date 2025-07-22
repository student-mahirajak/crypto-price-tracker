import requests

def fetch_crypto_prices(coin_ids):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(coin_ids),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}
