from models import User, UserStats, db

def fetch_user_by_email(email):
    """Fetch user by email."""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None, {"error": "User not found."}
    return user, None

def fetch_user_stats(user_id):
    """Fetch all stats for a specific user by user_id."""
    try:
        stats = UserStats.query.filter_by(user_id=user_id).all()
        if not stats:
            return None, {"error": "No stats found for the user.", "status": 404}
        return stats, None  # Return stats and None for error
    except Exception as e:
        return None, {"error": str(e), "status": 500}  # Handle unexpected exceptions

def delete_user_stats(user_id):
    """Delete all stats for a specific user by user_id."""
    try:
        UserStats.query.filter_by(user_id=user_id).delete()  # Delete user stats
        db.session.commit()  # Commit the deletion
        return {"message": "User stats deleted successfully."}, 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return {"error": str(e)}, 500
