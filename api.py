from flask import Flask, jsonify, request
import time
import random
import sqlite3
import logging
from flask_cors import CORS  # Allow frontend connections

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls from frontend

# Configure logging
logging.basicConfig(filename='api_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect('api_logs.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        timestamp TEXT, 
                        response_time FLOAT, 
                        status_code INT)''')
    return conn

@app.route('/api/test', methods=['GET'])
def test_api():
    start_time = time.time()

    # Simulate variable response times & random errors
    response_time = round(random.uniform(0.1, 2.5), 3)  # Random delay (0.1s to 2.5s)
    status_code = 500 if random.random() < 0.1 else 200  # 10% chance of failure
    
    time.sleep(response_time)

    try:
        # Insert log into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (timestamp, response_time, status_code) VALUES (datetime('now'), ?, ?)", 
                       (response_time, status_code))
        conn.commit()
    except Exception as e:
        logging.error(f"Database Error: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    finally:
        conn.close()

    # Log the request
    logging.info(f"API Call - Response Time: {response_time}s, Status: {status_code}")

    return jsonify({"message": "API response", "response_time": response_time, "status": status_code})

if __name__ == '__main__':
    app.run(debug=True)
