# constants and functions


# import modules
import requests
import json
from datetime import datetime
import math


# ------------ Constants ------------
const_symbol = 'btcusdt'
const_interval = '8h'
const_limit = 1000
const_mean_length = 20
const_long_mean_length = 200

# ------------ URLs ------------
# Funding
funding_rate_url = 'https://fapi.binance.com/fapi/v1/fundingRate'

# Candles
candle_url = 'https://fapi.binance.com/fapi/v1/klines'


# ------------ Funding Rates ------------
def get_funding_rate(symbol, limit):

    # define the endpoint URL
    url = funding_rate_url

    # define the payload
    payload = {
        'symbol': symbol,
        'limit': limit
    }

    # send the request
    response = requests.get(url, params=payload)

    # return the response
    return json.loads(response.text)


# ------------ Funding Data ------------
def get_funding_data(symbol, limit):

    # data
    funding_list = []
    funding = get_funding_rate(symbol=symbol, limit=limit)

    for x in funding:
        print('Testing X', x)
        time = x['fundingTime']
        funding = float(x['fundingRate'])
        symbol = x['symbol']

        funding_dict = {
            'timestamp': time,
            'funding_rate': funding,
            'symbol': symbol
        }

        funding_list.append(funding_dict)

    return funding_list


# ------------ Candle Sticks ------------
# Get klines for a given symbol.
def get_candles(symbol, interval, limit):

    # define the endpoint URL
    url = candle_url

    # define the payload
    payload = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    # send the request
    response = requests.get(url, params=payload)

    # return the response
    return json.loads(response.text)


# ------------ OHLC Candles ------------
def get_ohlc(symbol, interval, limit):

    # data
    candle_list = []
    candles = get_candles(symbol=symbol, interval=interval, limit=limit)

    for x in candles:

        open_time = x[0]
        open_price = float(x[1])
        high_price = float(x[2])
        low_price = float(x[3])
        close_price = float(x[4])
        close_time = x[6]

        candle_dict = {
            'symbol': symbol,
            'open_time': open_time,
            'close_time': close_time,
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price
        }

        candle_list.append(candle_dict)

    return candle_list


# ------------ Helpful Functions ------------
# Epoch milliseconds to human-readable
def epoch_milli_to_hr(epoch):
    return datetime.fromtimestamp(epoch/1000).strftime(
        '%d-%m-%Y %H:%M:%S'
    )


# Calculate standard deviation
def calculate_std_dev(data):

    n = 0  # number of elements
    mean = 0.0  # mean value
    m2 = 0.0  # sum of squared differences from the mean

    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        m2 += delta * delta2

    if n < 2:
        std_dev = float('nan')
    else:
        variance = m2 / (n - 1)
        std_dev = math.sqrt(variance)

    return std_dev


if __name__ == '__main__':
    get_funding_rate(symbol=const_symbol, limit=1),
    get_funding_data(symbol=const_symbol, limit=1),
    get_candles(symbol='symbol', interval='15m', limit=1),
    get_ohlc(symbol='symbol', interval='15m', limit=1)
