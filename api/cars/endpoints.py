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
    owner_id = request.args.get('owner_id', type=int)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT c.id, c.name, c.transmission, c.fuel_type, c.mileage, c.price, c.description, 
                     c.brand, c.year, c.color, c.seats, c.location, c.status,
                   c.image, c.image_2, c.image_3, c.image_4, c.image_5, c.created_at,
                   c.user_id AS seller_id,
                   u.name AS seller_name
            FROM cars c
            JOIN users u ON c.user_id = u.id
        """
        params = []
        if owner_id:
            query += " WHERE c.user_id = %s"
            params.append(owner_id)

        query += " ORDER BY c.created_at DESC"

        cursor.execute(query, params)
        cars = cursor.fetchall()

        # perbaiki path gambar
        for car in cars:
            for field in ['image', 'image_2', 'image_3', 'image_4', 'image_5']:
                if car.get(field):
                    car[field] = car[field].replace('\\', '/')

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
                   c.fuel_type, c.mileage, c.price, c.description, c.image, c.image_2, c.image_3, c.image_4, c.image_5, c.created_at, c.status,
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
    print("📥 request.form:", dict(request.form))
    print("📥 request.files:", request.files)
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
    image = required['image']
    image_2 = required['image_2']
    image_3 = required['image_3']
    image_4 = required['image_4']
    image_5 = required['image_5']

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

        return jsonify({
            "message": "Car added",
            "data": {
                "id": car_id,
                "user_id": user_id,
                "name": name,
                "brand": brand,
                "price": price,
                "mileage": mileage,
                "year": year,
                "transmission": transmission,
                "fuel_type": fuel_type,
                "color": color,
                "seats": seats,
                "location": location,
                "description": description,
                "image": image,
                "image_2": image_2,
                "image_3": image_3,
                "image_4": image_4,
                "image_5": image_5,
            }
        }), 201
    except Exception as e:
        conn.rollback()
        print("DB Error:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# UPDATE car
@cars_endpoints.route('/update/<int:car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Ambil data existing
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        existing = cursor.fetchone()
        if not existing:
            return jsonify({"error": "Car not found"}), 404

        # Ambil data baru, jika None gunakan existing
        name = request.form.get("name") or existing["name"]
        price = request.form.get("price") or existing["price"]
        brand = request.form.get("brand") or existing["brand"]
        year = request.form.get("year") or existing["year"]
        color = request.form.get("color") or existing["color"]
        transmission = request.form.get("transmission") or existing["transmission"]
        seats = request.form.get("seats") or existing["seats"]
        location = request.form.get("location") or existing["location"]
        fuel_type = request.form.get("fuel_type") or existing["fuel_type"]
        mileage = request.form.get("mileage") or existing["mileage"]
        description = request.form.get("description") or existing["description"]
        status = request.form.get("status") or existing["status"]

        # Simpan gambar baru jika ada
        image = save_image(request.files.get('image')) or existing["image"]
        image_2 = save_image(request.files.get('image_2')) or existing["image_2"]
        image_3 = save_image(request.files.get('image_3')) or existing["image_3"]
        image_4 = save_image(request.files.get('image_4')) or existing["image_4"]
        image_5 = save_image(request.files.get('image_5')) or existing["image_5"]

        # Update query
        cursor.execute("""
            UPDATE cars
            SET name=%s, price=%s, brand=%s, year=%s, color=%s,
                transmission=%s, seats=%s, location=%s, fuel_type=%s,
                mileage=%s, description=%s, status=%s,
                image=%s, image_2=%s, image_3=%s, image_4=%s, image_5=%s
            WHERE id = %s
        """, (name, price, brand, year, color, transmission, seats, location, fuel_type,
              mileage, description, status,
              image, image_2, image_3, image_4, image_5, car_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Car updated", "car_id": car_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# DELETE car
@cars_endpoints.route('/<int:car_id>', methods=['DELETE'])
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