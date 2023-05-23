from flask import Flask, jsonify, request, Blueprint
import jwt
import datetime
import os

from db import read_db, update_db
from auth import admin_protected

products_routes = Blueprint("products", __name__, url_prefix="/products")

@products_routes.route("")
def list_products():
    rows = read_db("SELECT * FROM products")
    return jsonify(rows)

@products_routes.route('', methods=['POST'])
@admin_protected
def create_product():
    data = request.get_json()
    category_id = data.get('category_id')
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    insert_query = "INSERT INTO products (category_id, name, description, price) VALUES (%s, %s, %s, %s)"
    insert_data = (category_id, name, description, price)
    created_rows = update_db(insert_query, insert_data)
    return jsonify({'message': f"{created_rows} created_rows"})

@products_routes.route('<int:id>', methods=['PUT'])
@admin_protected
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'message': "No data provided"}), 400

    update_fields = []
    update_data = []

    for field in ['category_id', 'name', 'description', 'price']:
        if field in data:
            update_fields.append(f"{field} = %s")
            update_data.append(data[field])

    update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
    update_data.append(id)
    update_data = tuple(update_data)

    updated_rows = update_db(update_query, update_data)

    return jsonify({'message': f"{updated_rows} row(s) updated"})

@products_routes.route('<int:id>', methods=['DELETE'])
@admin_protected
def delete_product(id):
    delete_query = "DELETE FROM products WHERE id=%s;"
    delete_data = (id,)
    deleted_rows = update_db(delete_query, delete_data)
    return jsonify({'message': f"{deleted_rows} deleted_rows"})

