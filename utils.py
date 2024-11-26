#!/usr/bin/env python
import string
import random
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extract token part from "Bearer <token>"

        # If no token is provided, return an error
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            # Decode the token using the app's secret key
            data = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
            user_id = data['id']

            # Check if the user exists in the database
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'User not found!'}), 404
            
            # Attach the user to the current request context for further use
            request.user_id = user.id

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated_function

def generate_state_value(length=8):
    """Generate a random state value."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def format_json_response(Data):
    pass