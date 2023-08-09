from flask import Blueprint
from .data import get_data

api_bp = Blueprint('api', __name__)

@api_bp.route('/get_data/', methods=['GET'])
def api_get_data():
    return get_data()
