from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database_utils import fetch_user_by_email, delete_user_stats
from utils.auth_utils import role_required  # Import role-based access decorator


reset_history_bp = Blueprint('reset_history', __name__)

@reset_history_bp.route('/api/reset_history', methods=['DELETE'])
@jwt_required()
@role_required(['free'])  # Restrict access to premium users
def reset_history():
    email = get_jwt_identity()
    user, error_response = fetch_user_by_email(email)
    if error_response:
        return jsonify(error_response)

    response, status = delete_user_stats(user.id)
    return jsonify(response), status
