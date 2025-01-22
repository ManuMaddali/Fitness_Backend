from functools import wraps
from flask import request, jsonify

def validate_fields(data, required_fields):
    """Validate required fields in the request payload."""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return {"error": f"Missing fields: {', '.join(missing_fields)}"}, 400
    return None

def validate_request(required_fields):
    """Decorator for validating fields in the request payload."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.json
            validation_error = validate_fields(data, required_fields)
            if validation_error:
                return validation_error  # No jsonify here to avoid issues with Pytest
            return func(*args, **kwargs)
        return wrapper
    return decorator
