import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

class JaveirsIoTManager:
    def __init__(self, credentials_path: str = None):
        """Initializes Firebase Firestore connection for IoT and home defense logging."""
        try:
            if not firebase_admin._apps:
                if credentials_path and os.path.exists(credentials_path):
                    cred = credentials.Certificate(credentials_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # Fallback to application default credentials or environment configs
                    firebase_admin.initialize_app()
            
            self.db = firestore.client()
            print("IoT & Firebase memory subsystem initialized successfully, sir.")
        except Exception as e:
            print(f"Warning: Firebase initialization failed. Operating in local offline mode: {e}")
            self.db = None

    def update_device_state(self, device_id: str, status: str, metadata: dict = None):
        """Updates or registers an IoT node state in Firestore."""
        if not self.db:
            return "Database offline, sir. Action simulated locally."
        
        try:
            payload = {
                "device_id": device_id,
                "status": status,
                "timestamp": datetime.utcnow(),
                "metadata": metadata or {}
            }
            self.db.collection("iot_devices").document(device_id).set(payload, merge=True)
            return f"Device '{device_id}' state updated to '{status}', sir."
        except Exception as e:
            return f"Failed to update device state in database: {e}"

    def log_security_event(self, event_type: str, severity: str, details: str):
        """Logs a defense or security alert to Firebase."""
        if not self.db:
            return "Database offline. Security event logged locally."
        
        try:
            event_data = {
                "event_type": event_type,
                "severity": severity,
                "details": details,
                "timestamp": datetime.utcnow()
            }
            self.db.collection("security_logs").add(event_data)
            return f"Security event logged: [{severity.upper()}] {event_type}, sir."
        except Exception as e:
            return f"Critical error logging security event: {e}"

# Quick diagnostic block if executed independently
if __name__ == "__main__":
    iot = JaveirsIoTManager()
    print(iot.update_device_state("perimeter_cam_01", "ACTIVE", {"resolution": "1080p"}))
    
