from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User

def role_required(required_roles):
    """Decorator to enforce role-based access."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the authenticated user's email
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()

            if not user:
                return jsonify({"error": "User not found."}), 404

            # Check if the user's role is allowed
            if user.role not in required_roles:
                return jsonify({"error": f"Access restricted to {', '.join(required_roles)} roles."}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
