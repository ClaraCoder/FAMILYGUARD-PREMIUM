import sqlite3
import json
import hashlib
from datetime import datetime

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

DB_PATH = config['database']['path']

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS children
                 (id INTEGER PRIMARY KEY, 
                  name TEXT NOT NULL, 
                  device_id TEXT UNIQUE, 
                  age INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS locations
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  latitude REAL, 
                  longitude REAL, 
                  accuracy REAL, 
                  address TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  app_name TEXT, 
                  activity_type TEXT, 
                  duration INTEGER, 
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS screen_time
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  date DATE, 
                  total_time INTEGER,
                  app_usage TEXT,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (id INTEGER PRIMARY KEY, 
                  child_id INTEGER, 
                  alert_type TEXT, 
                  message TEXT, 
                  severity TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  acknowledged BOOLEAN DEFAULT FALSE,
                  FOREIGN KEY (child_id) REFERENCES children (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY, 
                  key TEXT UNIQUE, 
                  value TEXT)''')
    
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
    
    # Insert sample data for demonstration
    c.execute("INSERT OR IGNORE INTO children (name, device_id, age) VALUES ('Anak Contoh', 'device_demo_123', 12)")
    
    conn.commit()
    conn.close()
    print("Database setup completed successfully!")

if __name__ == '__main__':
    setup_database()
EOL
