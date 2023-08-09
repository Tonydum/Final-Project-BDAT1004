import requests
from pymongo import MongoClient
from datetime import datetime, timedelta
import time

def get_cryptocurrency_prices(api_key, api_secret):
    base_url = 'https://api.coinbase.com/v2/prices'
    cryptocurrencies = ['BTC', 'ETH', 'USDT', 'XRP', 'BNB', 'USDC', 'DOGE', 'ADA', 'SOL', 'TRX', 'MATIC', 'LTC', 'DOT', 'TON',
                        'WBTC', 'AVAX', 'BCH', 'DAi', 'SHIB', 'LINK', 'XLM', 'BUSD', 'LEO', 'UNI', 'XMR', 'ETC', 'OKB',
                        'FIL', 'MNT', 'LDO', 'APT', 'ARB', 'CRO', 'VET', 'NEAR', 'QNT', 'MKR', 'aMKRv2', 'AAVE', 'GRT',
                        'OP', 'ALGO', 'EGLD', 'SAND', 'STX', 'THETA', 'EOS', 'XDC', 'XTZ', 'IMX', 'SNX', 'APE', 'USDD']  # You can add more cryptocurrencies if needed

    price_data = []

    for currency in cryptocurrencies:
        url = f"{base_url}/{currency}-USD/spot"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'CB-ACCESS-SIGN': api_secret,
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            symbol = data['data']['base']
            price = float(data['data']['amount'])
            timestamp = datetime.utcnow().isoformat()  # Use UTC timestamp

            price_data.append({
                'timestamp': timestamp,
                'symbol': symbol,
                'price': price
            })
        else:
            print(f"Failed to fetch {currency} price. Status code: {response.status_code}")

    return price_data

def store_prices_in_mongodb(price_data):
    # Connect to MongoDB (adjust the connection string as needed)
    client = MongoClient('mongodb://tonydum126:Icenova22@ac-l1mncqa-shard-00-00.s8ode9n.mongodb.net:27017,ac-l1mncqa-shard-00-01.s8ode9n.mongodb.net:27017,ac-l1mncqa-shard-00-02.s8ode9n.mongodb.net:27017/?ssl=true&replicaSet=atlas-cioiiy-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['Cryptocurrency']
    collection = db['Cryptocurrency']

    # Insert the price data into the MongoDB collection
    result = collection.insert_many(price_data)
    print(f"{len(result.inserted_ids)} records inserted into MongoDB.")

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' and 'YOUR_API_SECRET' with your actual Coinbase API credentials
    api_key = '7iHVSKt1OEhLK9pO'
    api_secret = 'OVmV1jP9fWeieHvNZch0hnkP6lxywPZX'

    while True:
        prices = get_cryptocurrency_prices(api_key, api_secret)
        store_prices_in_mongodb(prices)
        
        # Fetch data every 24 hours
        time.sleep(24 * 60 * 60)  # Sleep for 24 hours
