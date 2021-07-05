#!/usr/bin/env python3

# import the Shrimpy library for crypto exchange websockets
import shrimpy
# input your Shrimpy public and private key
from config import shrimpy_public_key, shrimpy_private_key

# a sample error handler, it simply prints the incoming error
def error_handler(err):
    print(err)

exchanges_bbo = {}

# define the handler to manage the output stream
def handler(msg):
    bid_price = msg['content']['bids'][0]['price']
    ask_price = msg['content']['asks'][0]['price']
    exchanges_bbo[msg['exchange']] = {'bid': float(bid_price), 'ask': float(ask_price)}
    best_bid = 0.0
    best_ask = 100000.0
    best_bid_exchange = ''
    best_ask_exchange = ''
    for key, value in exchanges_bbo.items():
        if value['bid'] > best_bid:
            best_bid = value['bid']
            best_bid_exchange = key
        if value['ask'] < best_ask:
            best_ask = value['ask']
            best_ask_exchange = key
    if best_bid > best_ask:
        print("sell on " + best_bid_exchange + " for " + str(best_bid))
        print("buy on " + best_ask_exchange + " for " + str(best_ask))
    else:
        print("No Arbitrage Available")


# create the Shrimpy websocket client
api_client = shrimpy.ShrimpyApiClient(shrimpy_public_key, shrimpy_private_key)
print(api_client.get_status())
raw_token = api_client.get_token()
print(raw_token)
client = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])
print(client)

# connect to the Shrimpy websocket and subscribe
client.connect()

# select exchanges to arbitrage
exchanges = ["bittrex", "binance", "kucoin"]
pair = "btc-usdt"

# subscribe to the websockets for the given pair on each exchange
# for exchange in exchanges:
#     subscribe_data = {
#         "type": "subscribe",
#         "exchange": exchange,
#         "pair": pair,
#         "channel": "bbo"
#     }
#     client.subscribe(subscribe_data, handler)



subscribe_data = {
    "type": "subscribe",
    "exchange": "binance",
    "pair": pair,
    "channel": "bbo"
}
client.subscribe(subscribe_data, handler)
