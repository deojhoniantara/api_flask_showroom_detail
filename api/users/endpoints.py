from flask import Blueprint, request, jsonify
from db import get_db_connection
from helper.form_validation import get_form_data
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        return jsonify({"data": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET user by ID
@users_endpoints.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, phone, email, address FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "OK", "data": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# POST create user
@users_endpoints.route('/register', methods=['POST'])
def create_user():
    required = get_form_data(["name", "email", "password", "phone", "address"], request)
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
@jwt_required()
def update_user(user_id):
    # Ambil yang tidak kosong
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"message": "Not Found", "description": "User not found"}), 404

    query = "UPDATE users SET "
    params = []
    updates = []

    if name:
        updates.append("name = %s")
        params.append(name)
    if email:
        updates.append("email = %s")
        params.append(email)
    if phone:
        updates.append("phone = %s")
        params.append(phone)
    if address:
        updates.append("address = %s")
        params.append(address)
    if password:
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        updates.append("password = %s")
        params.append(hashed_pw)

    if not updates:
        return jsonify({"message": "No changes provided"}), 400

    query += ", ".join(updates) + " WHERE id = %s"
    params.append(user_id)

    cursor.execute(query, tuple(params))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "OK",
        "description": "User updated successfully",
        "user_id": user_id,
        "name": name if name else user['name'],
        "email": email if email else user['email'],
        "phone": phone if phone else user['phone'],
        "address": address if address else user['address'],
    }), 200
 



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
