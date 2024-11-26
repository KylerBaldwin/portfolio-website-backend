# Flask Imports
from flask import Blueprint, jsonify

# Define the 'main' blueprint for general app-level routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"})

@main_bp.route("/projects", methods=['GET'])
def get_projects():
    return jsonify({"message": "This is the Projects Endpoint"})

@main_bp.route("/articles", methods=['GET'])
def get_articles():
    return jsonify({"message": "This is the Articles Endpoint"})
