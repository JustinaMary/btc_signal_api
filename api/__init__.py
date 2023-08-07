from flask import Blueprint
from .data import get_data

api_bp = Blueprint('api', __name__)

@api_bp.route('/get_data/<equity>', methods=['GET'])
def api_get_data(equity):
    return get_data(equity)
