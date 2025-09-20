mkdir -p modules

import sqlite3
import time
import threading
from datetime import datetime
from geopy.distance import geodesic

class LocationTracker:
    def __init__(self):
        self.db_path = "/data/data/com.termux/files/home/familyguard/familyguard.db"
        self.geofence_alerts = {}
    
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def update_location(self, child_id, latitude, longitude, accuracy, address):
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO locations (child_id, latitude, longitude, accuracy, address) VALUES (?, ?, ?, ?, ?)",
                     (child_id, latitude, longitude, accuracy, address))
            conn.commit()
            
            # Check geofences
            self.check_geofences(child_id, latitude, longitude)
            
        except Exception as e:
            print(f"Error updating location: {e}")
        finally:
            conn.close()
    
    def check_geofences(self, child_id, latitude, longitude):
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM geofences WHERE child_id = ?", (child_id,))
            geofences = c.fetchall()
            
            current_pos = (latitude, longitude)
            
            for geofence in geofences:
                fence_pos = (geofence['latitude'], geofence['longitude'])
                distance = geodesic(current_pos, fence_pos).meters
                
                if distance > geofence['radius']:
                    # Child is outside geofence
                    alert_key = f"{child_id}_{geofence['id']}"
                    
                    if alert_key not in self.geofence_alerts:
                        self.geofence_alerts[alert_key] = datetime.now()
                        self.create_alert(
                            child_id, 
                            "geofence", 
                            f"Anak keluar dari area {geofence['name']}",
                            "warning"
                        )
                else:
                    # Child is inside geofence, remove alert key if exists
                    alert_key = f"{child_id}_{geofence['id']}"
                    if alert_key in self.geofence_alerts:
                        del self.geofence_alerts[alert_key]
                        
        except Exception as e:
            print(f"Error checking geofences: {e}")
        finally:
            conn.close()
    
    def create_alert(self, child_id, alert_type, message, severity):
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO alerts (child_id, alert_type, message, severity) VALUES (?, ?, ?, ?)",
                     (child_id, alert_type, message, severity))
            conn.commit()
        except Exception as e:
            print(f"Error creating alert: {e}")
        finally:
            conn.close()
    
    def monitor_locations(self):
        """Background task to monitor locations and check for anomalies"""
        while True:
            try:
                # Implementasi monitoring logic di sini
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error in location monitoring: {e}")
                time.sleep(300)  # Wait 5 minutes on error

# Example usage
if __name__ == "__main__":
    tracker = LocationTracker()
    tracker.monitor_locations()
EOL
