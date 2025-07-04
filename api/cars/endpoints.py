import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

cars_endpoints = Blueprint('cars_endpoints', __name__)
UPLOAD_FOLDER = "img"

# GET all cars
@cars_endpoints.route('/', methods=['GET'])
def get_all_cars():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.id, c.name, c.brand, c.transmission, c.seats, c.year, c.color, c.location,
                   c.fuel_type, c.mileage, c.price, c.description, c.image, c.created_at,
                   u.id as owner_id, u.name as owner_name, u.email as owner_email
            FROM cars c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.created_at DESC
        """)
        cars = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify({"message": "OK", "data": cars}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET car by ID
@cars_endpoints.route('/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.name, c.brand, c.transmission, c.seats, c.year, c.color, c.location,
                   c.fuel_type, c.mileage, c.price, c.description, c.image, c.created_at,
                   u.id as owner_id, u.name as owner_name, u.email as owner_email
            FROM cars c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """, (car_id,))
        car = cursor.fetchone()
        cursor.close()
        conn.close()

        if car:
            return jsonify({"message": "OK", "data": car}), 200
        return jsonify({"message": "Car not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# CREATE new car
@cars_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create_car():
    required = get_form_data(["name", "price", "brand", "year", "color", "transmission",
                              "seats", "location", "fuel_type", "mileage"])
    name = required["name"]
    price = required["price"]
    brand = required["brand"]
    year = required["year"]
    color = required["color"]
    transmission = required["transmission"]
    seats = required["seats"]
    location = required["location"]
    fuel_type = required["fuel_type"]
    mileage = required["mileage"]
    description = request.form.get('description')
    image = request.form.get('image')

    user = get_jwt_identity()
    user_id = user['id'] if isinstance(user, dict) else user

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cars (user_id, name, brand, transmission, seats, year, color,
                              location, fuel_type, mileage, price, description, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, brand, transmission, seats, year, color, location,
              fuel_type, mileage, price, description, image))
        conn.commit()
        car_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({"message": "Car added", "car_id": car_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE car
@cars_endpoints.route('/update/<int:car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    required = get_form_data(["name", "price", "brand", "year", "color", "transmission",
                              "seats", "location", "fuel_type", "mileage"])
    name = required["name"]
    price = required["price"]
    brand = required["brand"]
    year = required["year"]
    color = required["color"]
    transmission = required["transmission"]
    seats = required["seats"]
    location = required["location"]
    fuel_type = required["fuel_type"]
    mileage = required["mileage"]
    description = request.form.get('description')
    image = request.form.get('image')

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE cars
            SET name=%s, brand=%s, transmission=%s, seats=%s, year=%s, color=%s,
                location=%s, fuel_type=%s, mileage=%s, price=%s, description=%s, image=%s
            WHERE id = %s
        """, (name, brand, transmission, seats, year, color, location, fuel_type,
              mileage, price, description, image, car_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Car updated", "car_id": car_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE car
@cars_endpoints.route('/delete/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Car deleted", "car_id": car_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
