from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token
from helper.db_helper import get_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
admins_endpoints = Blueprint('admins_endpoints', __name__)

@admins_endpoints.route('/login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if not admin:
        return jsonify({"msg": "Admin not found"}), 404

    if not bcrypt.check_password_hash(admin['password'], password):
        return jsonify({"msg": "Invalid password"}), 401

    access_token = create_access_token(
        identity=str(admin["id"]),
        additional_claims={
            'role': 'admin',
            'email': admin['email']
        }
    )
    decoded_token = decode_token(access_token)

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": decoded_token['exp'],
        "admin_id": admin["id"],
    }), 200
