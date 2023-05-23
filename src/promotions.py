from flask import Flask, jsonify, request, Blueprint
import jwt
import datetime
import os

from db import read_db, update_db
from auth import admin_protected

promotions_routes = Blueprint("promotions", __name__, url_prefix="/promotions")

@promotions_routes.route("")
def list_promotions():
    rows = read_db("SELECT * FROM promotions")
    return jsonify(rows)

@promotions_routes.route('', methods=['POST'])
@admin_protected
def create_product():
    data = request.get_json()
    product_id = data.get('product_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    discount = data.get('discount')

    insert_query = "INSERT INTO promotions (product_id, start_date, end_date, discount) VALUES (%s, %s, %s, %s)"
    insert_data = (product_id, start_date, end_date, discount)
    created_rows = update_db(insert_query, insert_data)
    return jsonify({'message': f"{created_rows} created_rows"})

@promotions_routes.route('<int:id>', methods=['PUT'])
@admin_protected
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'message': "No data provided"}), 400

    update_fields = []
    update_data = []

    for field in ['product_id', 'start_date', 'end_date', 'discount']:
        if field in data:
            update_fields.append(f"{field} = %s")
            update_data.append(data[field])

    update_query = f"UPDATE promotions SET {', '.join(update_fields)} WHERE id = %s"
    update_data.append(id)
    update_data = tuple(update_data)

    updated_rows = update_db(update_query, update_data)

    return jsonify({'message': f"{updated_rows} row(s) updated"})

@promotions_routes.route('<int:id>', methods=['DELETE'])
@admin_protected
def delete_product(id):
    delete_query = "DELETE FROM promotions WHERE id=%s;"
    delete_data = (id,)
    deleted_rows = update_db(delete_query, delete_data)
    return jsonify({'message': f"{deleted_rows} deleted_rows"})

