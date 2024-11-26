# Base Imports
import os
import dotenv
from datetime import timedelta
# Flask Imports
from flask import Flask
from flask_cors import CORS
# App Imports
import routes
from extensions import db

# Load environment variables
dotenv.load_dotenv()

def create_app():
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    app.permanent_session_lifetime = timedelta(days=7)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable modification tracking for performance
    app.secret_key = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    CORS(app)  # Enable CORS to allow requests from the React frontend

    # Register blueprints
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(routes.whoop_bp, url_prefix='/whoop')

    # Create all tables in the database
    with app.app_context():
        db.create_all()

    return app

# Create the Flask app instance
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)