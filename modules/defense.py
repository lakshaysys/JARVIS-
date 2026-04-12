import firebase_admin
from firebase_admin import firestore

class DefenseSystem:
    def __init__(self):
        """Initializes the connection to the Firestore database."""
        # This assumes firebase_admin.initialize_app() was called in main.py
        try:
            self.db = firestore.client()
            self.defense_mode = False
            print("[System] Security protocols loaded.")
        except Exception as e:
            print(f"[Error] Defense system failed to link to database: {e}")

    def toggle_defense_mode(self, status: bool):
        """
        Sets the J.A.V.E.I.R.S. security state and logs it to Firebase.
        """
        self.defense_mode = status
        state = "ACTIVE" if status else "DEACTIVATED"
        
        # Log the status change to your 'system_logs' collection in Firebase
        try:
            self.db.collection("system_logs").add({
                "event": "Defense Mode Toggle",
                "status": state,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"[Warning] Could not log to Firebase: {e}")

        return f"Defense Protocol {state}. All sensors are now monitoring for Master Lakshay."

    def check_intruder_alert(self):
        """Placeholder for future vision-based intruder detection."""
        if self.defense_mode:
            return "Scanning for unauthorized biometrics..."
        return "Defense mode is offline."