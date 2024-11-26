# Base Imports
import jwt
# Flask Imports
from flask import Blueprint, request, jsonify, current_app, session
# Application Imports
from models.user import User
from extensions import db
from utils import token_required
# Create the auth blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        # Generate JWT token (or session cookie)
        token = jwt.encode({'id': user.id}, current_app.secret_key, algorithm='HS256')
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route("/user", methods=['GET'])
@token_required
def admin_panel():
    user = User.query.get(session.get('user_id'))
    if user:
        return jsonify({
            'username': user.username,
            'email': user.email
        }), 200
    return jsonify({'message': 'User not found'}), 404