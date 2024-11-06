from app import app, db
from flask import jsonify, request
from models import Test

# Get all tests
@app.route("/test", methods=['GET'])
def get_all():
    tests = Test.query.all()
    # Assuming Test.to_json() is a valid method. It should be defined in the Test model.
    result = [test.to_json() for test in tests]  # Fixed variable name from `Test.to_json()` to `test.to_json()`
    return jsonify(result), 200  # Added status code for clarity

# Add data
@app.route("/test", methods=['POST'])
def create_new():
    try:
        print(request)
        data = request.json # This will work if the request is in JSON format
        name = data.get('name')

        if not name:  # Check if name is provided
            return jsonify({"error": "Name is required."}), 400  # Return a 400 error if name is missing

        new_test = Test(name=name)  # Changed variable name from `new` to `new_test` to avoid conflict with built-in `new`
        db.session.add(new_test)
        db.session.commit()

        return jsonify({"msg": "Committed successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500  # Return error message with status code 500