from flask import Blueprint, request, jsonify
from helper.db_helper import get_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bookings_endpoints = Blueprint('bookings_endpoints', __name__)

# GET all bookings
@bookings_endpoints.route('/read', methods=['GET'])
@jwt_required()
def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT b.id, u.name as user_name, c.name as car_name, b.booking_date, b.booking_time, b.location, b.status
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        LEFT JOIN cars c ON b.car_id = c.id
        ORDER BY b.created_at DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify({"message": "OK", "data": results}), 200

# GET bookings for current user
@bookings_endpoints.route('/my', methods=['GET'])
@jwt_required()
def get_my_bookings():
    user_id = get_jwt_identity()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT b.id, c.name as car_name, b.booking_date, b.booking_time, b.location, b.status
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
    """
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify({"message": "OK", "data": results}), 200

# CREATE booking
@bookings_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    car_id = request.form.get('car_id')  
    booking_date = request.form.get('booking_date')  
    booking_time = request.form.get('booking_time')  
    location = request.form.get('location')  
    message = request.form.get('message')  

    # Validate required fields
    if not all([car_id, booking_date, booking_time, location]):
        return jsonify({"msg": "car_id, booking_date, booking_time, and location are required"}), 400

    try:
        datetime.strptime(booking_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM cars WHERE id = %s", (car_id,))
    car = cursor.fetchone()
    if car and car['user_id'] == user_id:
        cursor.close()
        conn.close()
        return jsonify({"msg": "You cannot book your own car"}), 403

    # Insert booking
    insert_query = """
        INSERT INTO bookings (user_id, car_id, message, booking_date, booking_time, location)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (user_id, car_id, message, booking_date, booking_time, location))
    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Booking created successfully",
        "booking_id": new_id
    }), 201

# DELETE booking
@bookings_endpoints.route('/delete/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    user_id = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor()

    # Optional: validate ownership
    cursor.execute("SELECT id FROM bookings WHERE id = %s AND user_id = %s", (booking_id, user_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"msg": "Booking not found or access denied"}), 404

    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Booking deleted", "booking_id": booking_id}), 200
