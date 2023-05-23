from flask import Flask, jsonify, request
import jwt
import datetime
import os

from db import read_db
from auth import token_required

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route('/login', methods=['POST'])
def login():
    # Hardcoded email and password for now
    valid_email = 'soraya@gaillard.io'
    valid_password = 'abcdef'

    # Get the email and password from the request
    email = request.form.get('email')
    password = request.form.get('password')

    if email == valid_email and password == valid_password:
        # Create a JWT token
        token = jwt.encode({'user': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.environ['JWT_SECRET'])
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid email or password'}), 401

# Example route with token required
@app.route('/ping')
@token_required
def protected_route():
    return jsonify({'message': 'pong'})


@app.route("/products")
def list_products():
    request = "SELECT * FROM products"

    rows = read_db(request)

    # Return the rows as a JSON response
    return jsonify(rows)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
