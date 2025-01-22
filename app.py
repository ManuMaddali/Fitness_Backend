import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db
from datetime import timedelta

# Initialize global extensions

bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

# Load environment variables
load_dotenv()

def create_app():
    """App factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Dynamic Database Configuration
    if os.getenv("FLASK_ENV") == "testing":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance/users.db')}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)  # Set to 12 hours

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    print("App Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])  # Debug log

    # Register blueprints
    with app.app_context():
        db.create_all()  # Ensure tables are created
        from routes.register import register_bp
        from routes.hydration import hydration_bp
        from routes.bmr import bmr_bp
        from routes.history import history_bp
        from routes.reset_history import reset_history_bp
        from routes.full_coach import full_coach_bp
        from routes.coach import coach_bp
        from routes.login import login_bp

        app.register_blueprint(register_bp)
        app.register_blueprint(hydration_bp)
        app.register_blueprint(bmr_bp)
        app.register_blueprint(history_bp)
        app.register_blueprint(reset_history_bp)
        app.register_blueprint(full_coach_bp)
        app.register_blueprint(coach_bp)
        app.register_blueprint(login_bp)

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
