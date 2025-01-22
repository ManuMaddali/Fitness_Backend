from flask import Blueprint, request, jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from utils.database_utils import fetch_user_by_email
from utils.validation_utils import validate_request

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
@validate_request(['email', 'password'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    # Fetch user from database
    user, error_response = fetch_user_by_email(email)
    if error_response:
        return jsonify({"error": "Invalid email or password."}), 401

    # Verify password
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password."}), 401

    # Generate JWT token
    access_token = create_access_token(identity=email)
    return jsonify({"message": "Login successful.", "access_token": access_token}), 200
