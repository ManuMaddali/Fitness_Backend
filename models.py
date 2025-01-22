from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='free')  # Role column

    # Relationships
    stats = db.relationship('UserStats', backref='user', lazy=True)
    interactions = db.relationship('UserInteractions', lazy=True, overlaps="user")

class UserStats(db.Model):
    __tablename__ = 'user_stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE", name="fk_user_stats_user_id"),
        nullable=False
    )
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    tdee = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    bfp = db.Column(db.Float, nullable=False)
    bmr = db.Column(db.Float, nullable=False)
    ibw = db.Column(db.Float, nullable=False)
    hydration = db.Column(db.Float, nullable=False)

class UserInteractions(db.Model):
    __tablename__ = 'user_interactions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE", name="fk_user_interactions_user_id"),
        nullable=False
    )
    query = db.Column(db.String(500), nullable=False)
    FCgoal = db.Column(db.String(255), nullable=True)  # New field to store the goal
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    CBgoal = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, nullable=True)
    query_type = db.Column(db.String(50), nullable=True)  # Add this field for filtering interactions

    # Relationship
    user = db.relationship('User', lazy=True, overlaps="interactions")

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key to the Users table
    preferences = db.Column(db.JSON, nullable=True)  # Store preferences as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='preferences')

class PromptTemplate(db.Model):
    __tablename__ = 'prompt_templates'
    __table_args__ = {'extend_existing': True}  # Allow redefinition if already exists
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    template = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
