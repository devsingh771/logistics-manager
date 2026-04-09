import os
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops')

mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS shipment_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            log_entry TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        mysql.connection.commit()  
        cur.close()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # Fetch logs in descending order so the newest is on top
    cur.execute('SELECT log_entry, timestamp FROM shipment_logs ORDER BY id DESC')
    logs = cur.fetchall()
    cur.close()
    return render_template('index.html', logs=logs)

@app.route('/update-status', methods=['POST'])
def update_status():
    status_text = request.form.get('new_message')
    ports = ["Singapore Terminal", "Rotterdam Port", "Dubai Jebel Ali", "Port of Shanghai", "Los Angeles Hub"]
    
    # Custom Functional Extension: Formatting the entry
    location = random.choice(ports)
    formatted_entry = f"{location} | STATUS: {status_text.upper()}"
    
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO shipment_logs (log_entry) VALUES (%s)', [formatted_entry])
    mysql.connection.commit()
    cur.close()
    return jsonify({'entry': formatted_entry})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
