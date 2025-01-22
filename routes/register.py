from flask import Blueprint, request, jsonify
from utils.validation_utils import validate_request
from models import db, User
from flask_bcrypt import generate_password_hash

register_bp = Blueprint('register', __name__)

@register_bp.route('/api/register', methods=['POST'])
@validate_request(['email', 'password'])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists."}), 400

    # Create new user
    hashed_password = generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201
