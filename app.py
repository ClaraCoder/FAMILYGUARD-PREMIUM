from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file
from flask_cors import CORS
import sqlite3
import json
import threading
import time
from datetime import datetime, timedelta
import hashlib
import os
import logging
from cryptography.fernet import Fernet
import base64
from geopy.distance import geodesic
import pandas as pd
import numpy as np
from modules.location_tracker import LocationTracker
from modules.content_filter import ContentFilter
from modules.screen_time import ScreenTimeManager
from modules.alert_system import AlertSystem

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FamilyGuard')

app = Flask(__name__)
CORS(app)

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

app.secret_key = config['security']['secret_key']
DB_PATH = config['database']['path']

# Initialize modules
location_tracker = LocationTracker()
content_filter = ContentFilter()
screen_time_manager = ScreenTimeManager()
alert_system = AlertSystem()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Children table
    c.execute('''CREATE TABLE IF NOT EXISTS children
                 (id INTEGER PRIMARY KEY, 
                  name TEXT NOT NULL, 
                  device_id TEXT UNIQUE, 
                  age INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Locations table
    c.execute('''CREATE TABLE IF NOT EXISTS locations
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  latitude REAL, 
                  longitude REAL, 
                  accuracy REAL, 
                  address TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    # Activities table
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  app_name TEXT, 
                  activity_type TEXT, 
                  duration INTEGER, 
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    # Screen time table
    c.execute('''CREATE TABLE IF NOT EXISTS screen_time
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  date DATE, 
                  total_time INTEGER,
                  app_usage TEXT,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    # Alerts table
    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  alert_type TEXT, 
                  message TEXT, 
                  severity TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  acknowledged BOOLEAN DEFAULT FALSE,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    # Settings table
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY, 
                  key TEXT UNIQUE, 
                  value TEXT)''')
    
    # Geofences table
    c.execute('''CREATE TABLE IF NOT EXISTS geofences
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  name TEXT, 
                  latitude REAL, 
                  longitude REAL, 
                  radius INTEGER,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    # Insert default settings
    hashed_password = hashlib.sha256(config['security']['admin_password'].encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('admin_password', ?)", (hashed_password,))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('location_interval', '10')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('max_screen_time', ?)", (str(config['limits']['max_screen_time']),))
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Routes
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_db_connection()
        setting = conn.execute("SELECT value FROM settings WHERE key = 'admin_password'").fetchone()
        conn.close()
        
        if setting and setting['value'] == hashed_password:
            session['logged_in'] = True
            session['login_time'] = datetime.now().isoformat()
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/anak')
def anak_page():
    return render_template('anak.html')

@app.route('/settings')
def settings_page():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/alerts')
def alerts_page():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('alerts.html')

# API Routes
@app.route('/api/children', methods=['GET', 'POST'])
def api_children():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    
    if request.method == 'GET':
        children = conn.execute('SELECT * FROM children').fetchall()
        result = [dict(child) for child in children]
        conn.close()
        return jsonify(result)
    
    elif request.method == 'POST':
        data = request.json
        try:
            c = conn.cursor()
            c.execute("INSERT INTO children (name, device_id, age) VALUES (?, ?, ?)",
                     (data['name'], data['device_id'], data.get('age', 0)))
            conn.commit()
            child_id = c.lastrowid
            conn.close()
            return jsonify({'status': 'success', 'child_id': child_id})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Device already registered'})

# ... (Tambahkan lebih banyak endpoint API sesuai kebutuhan)

def start_server():
    logger.info("Starting FamilyGuard Premium Server...")
    init_db()
    
    # Start background tasks
    threading.Thread(target=alert_system.monitor_alerts, daemon=True).start()
    threading.Thread(target=location_tracker.monitor_locations, daemon=True).start()
    
    # Run the Flask app
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['server']['debug']
    )

if __name__ == '__main__':
    start_server()
EOL
