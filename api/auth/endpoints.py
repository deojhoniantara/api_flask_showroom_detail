"""Routes for authentication"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token
from helper.db_helper import get_connection  
from flask_jwt_extended import jwt_required
from flask_bcrypt import Bcrypt

auth_endpoints = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_endpoints.route('/login', methods=['POST'])
def login():
    """Login route for users"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Verify password with bcrypt
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"msg": "Invalid password"}), 401

    # Generate token
    access_token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            'email': user["email"]
        }
    )

    expires = decode_token(access_token)['exp']

    return jsonify({
        "access_token": access_token,
        "expires_in": expires,
        "token_type": "Bearer"
    }), 200

@auth_endpoints.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful. Please remove token on client side."}), 200
