import os
import time
from flask import Blueprint, jsonify, request, current_app
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename


cars_endpoints = Blueprint('cars_endpoints', __name__)
UPLOAD_FOLDER = "img"

# GET all cars
@cars_endpoints.route('/', methods=['GET'])
def get_all_cars():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.id, c.name, c.transmission, c.fuel_type, c.mileage, c.price, c.description, c.image, c.created_at
            FROM cars c
            ORDER BY c.created_at DESC
        """)
        cars = cursor.fetchall()
        for car in cars:
            if car['image']:
                car['image'] = car['image'].replace('\\', '/')


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
                   c.fuel_type, c.mileage, c.price, c.description, c.image, c.image_2, c.image_3, c.image_4, c.image_5, c.created_at,
                   u.id as owner_id, u.name as owner_name, u.email as owner_email
            FROM cars c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """, (car_id,))
        car = cursor.fetchone()
        if car['image']:
            car['image'] = car['image'].replace('\\', '/')

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
                              "seats", "location", "fuel_type", "mileage", 
                              "image", "image_2", "image_3", "image_4", "image_5"], request)
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
    image = required('image')
    image_2 = required('image_2')
    image_3 = required('image_3')
    image_4 = required('image_4')
    image_5 = required('image_5')

    user = get_jwt_identity()
    user_id = user['id'] if isinstance(user, dict) else user

    image = save_image(request.files.get('image'))  # dari <input type="file" name="image" />
    image_2 = save_image(request.files.get('image_2'))
    image_3 = save_image(request.files.get('image_3'))
    image_4 = save_image(request.files.get('image_4'))
    image_5 = save_image(request.files.get('image_5'))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cars (user_id, name, brand, transmission, seats, year, color,
                              location, fuel_type, mileage, price, description, image, image_2, image_3, image_4, image_5)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, brand, transmission, seats, year, color, location,
              fuel_type, mileage, price, description, image, image_2, image_3, image_4, image_5))
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
    try:
        name = request.form.get("name")
        price = request.form.get("price")
        brand = request.form.get("brand")
        year = request.form.get("year")
        color = request.form.get("color")
        transmission = request.form.get("transmission")
        seats = request.form.get("seats")
        location = request.form.get("location")
        fuel_type = request.form.get("fuel_type")
        mileage = request.form.get("mileage")
        description = request.form.get("description")

        image = save_image(request.files.get('image'))
        image_2 = save_image(request.files.get('image_2'))
        image_3 = save_image(request.files.get('image_3'))
        image_4 = save_image(request.files.get('image_4'))
        image_5 = save_image(request.files.get('image_5'))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT image, image_2, image_3, image_4, image_5 FROM cars WHERE id = %s", (car_id,))
        existing = cursor.fetchone()

        updated_image = image or existing[0]
        updated_image_2 = image_2 or existing[1]
        updated_image_3 = image_3 or existing[2]
        updated_image_4 = image_4 or existing[3]
        updated_image_5 = image_5 or existing[4]

        cursor.execute("""
            UPDATE cars
            SET name=%s, price=%s, brand=%s, year=%s, color=%s,
                transmission=%s, seats=%s, location=%s, fuel_type=%s,
                mileage=%s, description=%s, image=%s, image_2=%s, image_3=%s, image_4=%s, image_5=%s
            WHERE id = %s
        """, (name, price, brand, year, color, transmission, seats, location, fuel_type,
              mileage, description, updated_image, updated_image_2, updated_image_3, updated_image_4, updated_image_5, car_id))

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


def save_image(image_file):
    if image_file:
        filename = f"{int(time.time())}_{secure_filename(image_file.filename)}"
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        image_file.save(upload_path)
        return f"static/uploads/{filename}"
    return None