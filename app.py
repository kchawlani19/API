from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
from config import mysql_config

app = Flask(__name__)
bcrypt = Bcrypt(app)

mysql_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': '125411707@ab',
    'database': 'user_db'
}


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    # Hash the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert user data into the database
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Login failed. Check your email and password."})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app,host="0.0.0.0",port=8000)
