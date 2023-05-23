from flask import Flask, jsonify, request
import jwt
import datetime
import os

from db import read_db, update_db
from auth import admin_protected

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

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

@app.route('/products', methods=['POST'])
@admin_protected
def create_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    insert_query = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
    insert_data = (name, description, price)
    created_rows = update_db(insert_query, insert_data)
    return jsonify({'message': f"{created_rows} created_rows"})

@app.route('/products/<int:id>', methods=['PUT'])
@admin_protected
def update_product(id):
    data = request.get_json()

    # Check if any data is provided
    if not data:
        return jsonify({'message': "No data provided"}), 400

    update_fields = []
    update_data = []

    for field in ['name', 'description', 'price']:
        if field in data:
            update_fields.append(f"{field} = %s")
            update_data.append(data[field])

    update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
    update_data.append(id)
    update_data = tuple(update_data)

    updated_rows = update_db(update_query, update_data)

    if updated_rows > 0:
        return jsonify({'message': f"{updated_rows} row(s) updated"})
    else:
        return jsonify({'message': f"No product found with id {id}"}), 404

@app.route('/products/<int:id>', methods=['DELETE'])
@admin_protected
def delete_product(id):
    delete_query = "DELETE FROM products WHERE id=%s;"
    delete_data = (id,)
    deleted_rows = update_db(delete_query, delete_data)
    return jsonify({'message': f"{deleted_rows} deleted_rows"})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
