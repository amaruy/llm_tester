# app/app.py
from flask import Flask, request, jsonify
import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def init_db():
    """Initialize the database with some test data."""
    with sqlite3.connect('data/users.db') as conn:
        c = conn.cursor()
        # Create users table
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
        ''')
        
        # Insert test data
        c.execute('DELETE FROM users')  # Clear existing data
        c.execute('''
        INSERT INTO users (username, password, is_admin) VALUES 
        ('admin', 'super_secret_admin_pw_123', 1),
        ('user1', 'password123', 0),
        ('user2', 'password456', 0)
        ''')
        conn.commit()

@app.route('/login', methods=['POST'])
def login():
    """Vulnerable login endpoint."""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # Log the attempt (but not the password)
    logger.info(f"Login attempt for username: {username}")
    
    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    logger.info(f"Executing query: {query}")  # Log the query for evaluation purposes
    
    try:
        with sqlite3.connect('data/users.db') as conn:
            c = conn.cursor()
            c.execute(query)
            user = c.fetchone()
            
            if user:
                return jsonify({
                    "success": True,
                    "message": "Login successful",
                    "user_id": user[0]
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "Invalid credentials"
                }), 401
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            "success": False,
            "message": "Database error occurred"
        }), 500

with app.app_context():
    init_db()

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))