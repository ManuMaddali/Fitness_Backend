from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database_utils import fetch_user_by_email, fetch_user_stats
from utils.auth_utils import role_required  # Import role-based access decorator
from models import db, UserInteractions

history_bp = Blueprint('history', __name__)

@history_bp.route('/api/history', methods=['GET'])
@jwt_required()
def get_user_history():
    user_id = get_jwt_identity()
    interactions = db.session.query(UserInteractions).filter_by(user_id=user_id).order_by(
        UserInteractions.timestamp.desc()).all()
    
    history = []
    for interaction in interactions:
        history.append({
            "query": interaction.query,
            "response": interaction.response,
            "query_type": interaction.query_type,
            "FCgoal": interaction.goal,  # Include the goal in the response
            "timestamp": interaction.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "feedback": interaction.feedback
        })

    return jsonify({"success": True, "data": history}), 200
