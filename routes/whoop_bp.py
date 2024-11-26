# Base Imports
import os
# Flask Imports
from flask import Blueprint, jsonify, redirect, session, request, url_for
from whoop.whoop_api import Whoop
# App Imports
from utils import generate_state_value
from models import User
from extensions import db
# Create the whoop blueprint
whoop_bp = Blueprint('whoop', __name__)

whoop = Whoop(client_id=os.getenv('CLIENT_ID'),
                        client_secret=os.getenv('CLIENT_SECRET'))

# Redirect to Whoop Authorization endpoint
@whoop_bp.route("/auth", methods=['GET'])
def whoop_auth():
    state = generate_state_value()
    session['oauth_state'] = state
    authorization_url = f"{whoop.authorization_url}&state={state}"
    return redirect(authorization_url)

# Authorize whoop client and fetch tokens
@whoop_bp.route("/oauth2_callback", methods=['GET'])
def callback():
    state = request.args.get('state')
    code = request.args.get('code')

    # Validate state to prevent CSRF
    if not state or state != session.get('oauth_state'):
        return jsonify({'message': 'Invalid state'}), 400

    try:
        # Exchange code for access token
        token_response = whoop.get_access_token(authorization_code=code)
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve access token from Whoop', 'error': str(e)}), 500

    refresh_token = token_response.get('refresh_token')

    # Check if we have the tokens
    if not refresh_token:
        return jsonify({'message': 'Refresh token missing'}), 400

    # Assuming user ID is in the session, associate the tokens with the user
    #user_id = session.get('user_id')
    #if not user_id:
    #    return jsonify({'message': 'User not authenticated'}), 401

    user = User.query.get(1)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.whoop_refresh = refresh_token
    db.session.commit()

    # Redirect the user to a success page in the frontend
    return redirect("https://kylerbaldwin.com/whoop/success?status=ok")