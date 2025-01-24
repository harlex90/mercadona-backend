from flask import Flask, jsonify, request, Blueprint
import jwt
import datetime
import os

from db import read_db, update_db
from auth import admin_protected

categories_routes = Blueprint("categories", __name__, url_prefix="/categories")

@categories_routes.route("")
def list_categories():
    rows = read_db("SELECT * FROM categories")
    return jsonify(rows)

@categories_routes.route("<int:id>")
def show_product(id):
    rows = read_db(f"SELECT * FROM categories WHERE id = {id} LIMIT 1")
    if len(rows) < 1:
        return jsonify({ "error": 404 })
    return jsonify(rows[0])

@categories_routes.route('', methods=['POST'])
@admin_protected
def create_category():
    data = request.get_json()
    name = data.get('name')

    

    insert_query = "INSERT INTO categories (name) VALUES (%s)"
    insert_data = (name,)
    created_rows = update_db(insert_query, insert_data)
    return jsonify({'message': f"{created_rows} created_rows"})

@categories_routes.route('<int:id>', methods=['PUT'])
@admin_protected
def update_category(id):
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

@categories_routes.route('<int:id>', methods=['DELETE'])
@admin_protected
def delete_category(id):
    # delete products from category
    delete_products_query = "DELETE FROM products WHERE category_id=%s;"
    delete_products_data = (id,)
    deleted_products_rows = update_db(delete_products_query, delete_products_data)
    # delete the category
    delete_category_query = "DELETE FROM categories WHERE id=%s;"
    delete_category_data = (id,)
    deleted_category_rows = update_db(delete_category_query, delete_category_data)
    return jsonify({'message': f"{deleted_category_rows} deleted_rows"})

     

