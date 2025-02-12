from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)

class model:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin",
                database="user",
                port="3306",
                autocommit=True
            )
            self.cursor = self.db.cursor(dictionary=True)
            print("Connected to database")
        except mysql.connector.Error as e:
            print(f"Couldn't connect to database: {e}")
            self.db = None
            self.cursor = None
    
    def json_response(self, data, status=200):
        return jsonify(data), status

    def get_all_users(self):
        if not self.cursor:
            return self.json_response({"error": "Database down"}, 500)
        
        try:
            self.cursor.execute("SELECT * FROM users")
            users = self.cursor.fetchall()
            return self.json_response(users)
        except mysql.connector.Error as e:
            return self.json_response({"error": str(e)}, 500)

    def update_user_model(self, data):
        if not self.cursor:
            return self.json_response({"error": "Database down"}, 500)
        
        try:
            user_id = data.get('id')
            if not user_id:
                return self.json_response({"error": "Need user ID"}, 400)
            
            self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = self.cursor.fetchone()
            if not user:
                return self.json_response({"error": "User not found"}, 404)
            
            #update fields
            updates = {
                'name': data.get('name', user['name']),
                'email': data.get('email', user['email']),
                'password': data.get('password', user['password'])
            }
            
            self.cursor.execute(
                "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s",
                (updates['name'], updates['email'], updates['password'], user_id)
            )
            
            return self.json_response({"status": "ok"})
            
        except mysql.connector.Error as e:
            return self.json_response({"error": str(e)}, 500)

    def delete_user_model(self, data):
        if not self.cursor:
            return self.json_response({"error": "Database down"}, 500)
            
        try:
            user_id = data.get('id')
            if not user_id:
                return self.json_response({"error": "Need user ID"}, 400)
                
            self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            if self.cursor.rowcount:
                return self.json_response({"status": "ok"})
            return self.json_response({"error": "User not found"}, 404)
            
        except mysql.connector.Error as e:
            return self.json_response({"error": str(e)}, 500)

    def login_model(self, data):
        if not self.cursor:
            return self.json_response({"error": "Database down"}, 500)
            
        try:
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return self.json_response({"error": "Need email and password"}, 400)
            
            self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = self.cursor.fetchone()
            
            if not user or not check_password_hash(user['password'], password):
                return self.json_response({"error": "Wrong email or password"}, 401)
            
            token = create_access_token(
                identity=user['id'],
                additional_claims={'email': user['email'], 'name': user['name']}
            )
            
            return self.json_response({
                "status": "ok",
                "token": token,
                "user": {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email']
                }
            })
            
        except mysql.connector.Error as e:
            return self.json_response({"error": str(e)}, 500)

    def register_model(self, data):
        if not self.cursor:
            return self.json_response({"error": "Database down"}, 500)
            
        try:
            if not all(k in data for k in ['name', 'email', 'password']):
                return self.json_response({"error": "Missing required fields"}, 400)
                
            hashed_pw = generate_password_hash(data['password'])
            
            self.cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (data['name'], data['email'], hashed_pw)
            )
            
            return self.json_response({"status": "ok"}, 201)
            
        except mysql.connector.Error as e:
            return self.json_response({"error": str(e)}, 500)