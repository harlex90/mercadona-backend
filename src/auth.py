from functools import wraps
from flask import jsonify, request
import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

# A decorator function to check if the JWT token is valid
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the token is in the header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')

        # If the token is not present, return an error
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        # Verify the token
        try:
            jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])
        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        except Exception as e:
            # return jsonify({'message': f'Error: {str(e)}'}), 401 # debug purpose
            return jsonify({'message': 'Token is invalid'}), 401


        return f(*args, **kwargs)

    return decorated
