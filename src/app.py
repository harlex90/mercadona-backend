from flask import Flask, jsonify, request
import jwt
import datetime
import os

from db import read_db
from auth import admin_protected

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # find user in db
    users = read_db(f"SELECT * FROM `admins` WHERE email='{email}' LIMIT 1;")
    if len(users) < 1:
        return jsonify({'message': 'Invalid email or password'}), 401
    user = users[0]

    if email == user['email'] and password == user['password']:
        # Create a JWT token
        token = jwt.encode({'user': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.environ['JWT_SECRET'])
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid email or password'}), 401

# Example route with token required
@app.route('/ping')
@admin_protected
def protected_route():
    return jsonify({'message': 'pong'})


@app.route("/products")
def list_products():
    rows = read_db("SELECT * FROM products")
    return jsonify(rows)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
