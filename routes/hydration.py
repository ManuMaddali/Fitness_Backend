from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_utils import role_required


hydration_bp = Blueprint('hydration', __name__)

@hydration_bp.route('/api/hydration', methods=['POST'])
@jwt_required()
@role_required(['free', 'premium'])  # Free and premium users can access this endpoint
def calculate_hydration():
    data = request.json
    weight_lbs = data.get('weight')
    activity_level = data.get('activity_level')
    gender = data.get('gender', '').lower()

    # Validate inputs
    if not all([weight_lbs, activity_level, gender]):
        return jsonify({"error": "Weight, activity level, and gender are required."}), 400

    activity_levels = {
        "sedentary": 1.2,
        "light activity": 1.375,
        "moderate activity": 1.55,
        "very active": 1.725,
        "extremely active": 1.9
    }

    activity_multiplier = activity_levels.get(activity_level.lower())
    if not activity_multiplier:
        return jsonify({"error": f"Invalid activity level. Options: {', '.join(activity_levels.keys())}"}), 400

    # Calculate hydration
    weight_kg = weight_lbs / 2.20462
    hydration = weight_kg * 0.033 * activity_multiplier
    if gender == 'male':
        hydration += 0.5
    elif gender == 'female':
        hydration += 0.3

    return jsonify({
        "hydration": round(hydration, 2),
        "message": "This is your daily hydration need based on weight, gender, and activity level."
    }), 200
