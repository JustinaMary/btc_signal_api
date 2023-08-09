from flask import jsonify
from utils import live_trading

def get_data():
    data = live_trading.luke()
    return jsonify(data), 200

