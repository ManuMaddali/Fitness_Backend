from flask import Blueprint, request, jsonify
from utils.database_utils import fetch_user_by_email
from utils.validation_utils import validate_fields
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    validation_error = validate_fields(data, ['email', 'password'])
    if validation_error:
        return jsonify(validation_error)

    email = data['email']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 200


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    validation_error = validate_fields(data, ['email', 'password'])
    if validation_error:
        return jsonify(validation_error)

    email = data['email']
    password = data['password']

    user, error_response, status = fetch_user_by_email(email)
    if not user:
        return jsonify(error_response), status

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password."}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"message": "Login successful.", "access_token": access_token}), 200
