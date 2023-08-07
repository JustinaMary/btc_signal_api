from flask import jsonify
from utils import live_trading

def get_data(equity):
    data = live_trading.luke(int(equity))
    return jsonify(data), 200

