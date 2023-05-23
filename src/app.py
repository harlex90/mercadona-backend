from flask import Flask, jsonify
from db import read_db

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/products")
def list_products():
    request = "SELECT * FROM products"

    rows = read_db(request)

    # Return the rows as a JSON response
    return jsonify(rows)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
