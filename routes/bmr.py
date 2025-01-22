from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_utils import role_required


bmr_bp = Blueprint('bmr', __name__)

@bmr_bp.route('/api/bmr', methods=['POST'])
@jwt_required()
@role_required(['free', 'premium'])  # Free and premium users can access this endpoint
def calculate_bmr():
    data = request.json
    weight_lbs = data.get('weight')
    height_feet = data.get('height_feet')
    height_inches = data.get('height_inches')
    age = data.get('age')
    gender = data.get('gender', '').lower()

    # Validate inputs
    if not all([weight_lbs, height_feet, height_inches, age, gender]):
        return jsonify({"error": "All fields are required."}), 400

    weight_kg = weight_lbs / 2.20462
    height_cm = ((height_feet * 12) + height_inches) * 2.54

    if gender == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    elif gender == 'female':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        return jsonify({"error": "Invalid gender. Must be 'male' or 'female'."}), 400

    return jsonify({
        "bmr": round(bmr, 2),
        "message": "This is your Basal Metabolic Rate (BMR) based on your input data."
    }), 200
