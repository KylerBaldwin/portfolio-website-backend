from datetime import timedelta

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models.user import User
from extensions import db

# Create the auth blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Hash password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate the user and issue a JWT stored in an HttpOnly cookie.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Authenticate user
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Create access token
        access_token = create_access_token(identity={'id': user.id, 'username': user.username}, 
                                           expires_delta=timedelta(hours=1))

        # Set the token in an HttpOnly cookie
        response = jsonify({'message': 'Login successful'})
        response.set_cookie(
            'access_token_cookie',
            access_token,
            httponly=True,
            secure=True,  # Set True in production (requires HTTPS)
            samesite='Lax'
        )
        return response

    return jsonify({'message': 'Invalid username or password'}), 401


@auth_bp.route('/user', methods=['GET'])
@jwt_required(locations=["cookies"])
def user_profile():
    """
    Fetch the currently authenticated user's profile using the JWT in the cookie.
    """
    identity = get_jwt_identity()  # Get user identity from JWT
    user_id = identity.get('id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Clear the authentication cookie.
    """
    response = jsonify({'message': 'Logout successful'})
    response.delete_cookie('access_token_cookie')
    return response