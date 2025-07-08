from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

articles_endpoints = Blueprint('articles_endpoints', __name__)

# GET all articles
@articles_endpoints.route('/read', methods=['GET'])
def read_articles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, admin_id, title, image, created_at 
        FROM articles 
        ORDER BY created_at DESC
    """)
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"message": "OK", "data": articles}), 200

# GET article by ID
@articles_endpoints.route('/read/<int:article_id>', methods=['GET'])
def read_article_by_id(article_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, admin_id, title, content, image, created_at 
        FROM articles 
        WHERE id = %s
    """, (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    if article:
        return jsonify({"message": "OK", "data": article}), 200
    return jsonify({"message": "Article not found"}), 404

# CREATE new article
@articles_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create_article():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin only"}), 403

    admin_id = get_jwt_identity()  

    # Gunakan get_form_data hanya untuk field text
    required = get_form_data(["title", "content"], request)
    try:
        title = required['title']
        content = required['content']
    except ValueError as ve:
        return jsonify({"msg": str(ve)}), 400

    # Ambil file gambar langsung dari request.files
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"msg": "Image is required"}), 400

    # Simpan gambar
    filename = secure_filename(f"{datetime.utcnow().timestamp()}_{image_file.filename}")
    upload_dir = os.path.join('static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    image_path = os.path.join(upload_dir, filename)
    image_file.save(image_path)
    image_path = image_path.replace('\\', '/')

    # Simpan data ke database
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO articles (admin_id, title, content, image) VALUES (%s, %s, %s, %s)",
            (admin_id, title, content, image_path)
        )
        conn.commit()
        article_id = cursor.lastrowid
        return jsonify({
            "msg": "Article created", 
            "article_id": article_id,
            "title": title,
            "content": content,
            "image": image_path
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# UPDATE article
@articles_endpoints.route('/update/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin only"}), 403

    admin_id = get_jwt_identity()

    title = request.form.get('title')
    content = request.form.get('content')
    image_file = request.files.get('image')
    image_path = None

    if image_file:
        filename = secure_filename(f"{datetime.utcnow().timestamp()}_{image_file.filename}")
        upload_dir = os.path.join('static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, filename)
        image_file.save(image_path)
        image_path = image_path.replace('\\', '/')

    if not all([title, content]):
        return jsonify({"msg": "title and content are required"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT image FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    old_image = article['image'] if article else None

    # Gunakan gambar lama jika tidak upload gambar baru
    final_image_path = image_path if image_path else old_image
    
    cursor.execute(
        "UPDATE articles SET title = %s, content = %s, image = %s WHERE id = %s",
        (title, content, final_image_path, article_id)
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Article not found"}), 404
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"msg": "Article updated", "article_id": article_id, "title": title}), 200

# DELETE article
@articles_endpoints.route('/delete/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':   
        return jsonify({"msg": "Admin only"}), 403

    admin_id = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Article not found"}), 404
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"msg": "Article deleted", "article_id": article_id}), 200


@articles_endpoints.route('/<int:article_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(article_id):
    user_id = get_jwt_identity()
    comment = request.form.get('comment')

    if not comment:
        return jsonify({'msg': 'Comment content is required'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO article_comments (article_id, user_id, comment) VALUES (%s, %s, %s)",
            (article_id, user_id, comment)
        )
        conn.commit()
        return jsonify({"message": "Comment added", "comment": comment}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@articles_endpoints.route('/<int:article_id>/comments', methods=['GET'])
def get_comments(article_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ac.id, ac.comment, ac.created_at, u.name AS user_name
        FROM article_comments ac
        JOIN users u ON ac.user_id = u.id
        WHERE ac.article_id = %s
        ORDER BY ac.created_at DESC
    """, (article_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'message': 'OK', 'data': comments}), 200
