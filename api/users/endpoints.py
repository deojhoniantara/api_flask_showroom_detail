from flask import Blueprint, request, jsonify
from db import get_db_connection
from helper.form_validation import get_form_data
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
users_endpoints = Blueprint('users_endpoints', __name__)

# GET all users
@users_endpoints.route('/', methods=['GET'])
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, phone, address, created_at FROM users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET user by ID
@users_endpoints.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, phone, address, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST create user
@users_endpoints.route('/register', methods=['POST'])
def create_user():
    required = get_form_data(["name", "email", "password", "phone", "address"])
    name = required["name"]
    email = required["email"]
    password = required["password"]
    phone = required["phone"]
    address = required["address"]

    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Conflict",
                "description": "User with this email already exists"
            }), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor.execute("""
            INSERT INTO users (name, email, password, phone, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, hashed_password, phone, address))
        conn.commit()
        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "message": "OK",
            "description": "User created successfully",
            "user_id": new_id,
            "name": name,
            "email": email
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT update user
@users_endpoints.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    required = get_form_data(["name", "email", "phone", "address"])
    name = required["name"]
    email = required["email"]
    phone = required["phone"]
    address = required["address"]
    password = request.form.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Not Found",
                "description": "User not found"
            }), 404

        cursor.execute("""
            UPDATE users SET name = %s, email = %s, password = %s, phone = %s, address = %s
            WHERE id = %s
        """, (name, email, password, phone, address, user_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "OK",
            "description": "User updated successfully",
            "user_id": user_id,
            "name": name,
            "email": email
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE user
@users_endpoints.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
