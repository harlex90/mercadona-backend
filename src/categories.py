from flask import Flask, jsonify, request, Blueprint
import jwt
import datetime
import os

from db import read_db, update_db
from auth import admin_protected

categories_routes = Blueprint("categories", __name__, url_prefix="/categories")

@categories_routes.route("/")
def list_categories():
    rows = read_db("SELECT * FROM categories")
    return jsonify(rows)

@categories_routes.route('/', methods=['POST'])
@admin_protected
def create_product():
    data = request.get_json()
    name = data.get('name')

    insert_query = "INSERT INTO categories (name) VALUES (%s)"
    insert_data = (name,)
    created_rows = update_db(insert_query, insert_data)
    return jsonify({'message': f"{created_rows} created_rows"})

@categories_routes.route('/<int:id>', methods=['PUT'])
@admin_protected
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'message': "No data provided"}), 400

    update_fields = []
    update_data = []

    for field in ['name']:
        if field in data:
            update_fields.append(f"{field} = %s")
            update_data.append(data[field])

    update_query = f"UPDATE categories SET {', '.join(update_fields)} WHERE id = %s"
    update_data.append(id)
    update_data = tuple(update_data)

    updated_rows = update_db(update_query, update_data)

    return jsonify({'message': f"{updated_rows} row(s) updated"})

@categories_routes.route('/<int:id>', methods=['DELETE'])
@admin_protected
def delete_product(id):
    delete_query = "DELETE FROM categories WHERE id=%s;"
    delete_data = (id,)
    deleted_rows = update_db(delete_query, delete_data)
    return jsonify({'message': f"{deleted_rows} deleted_rows"})

