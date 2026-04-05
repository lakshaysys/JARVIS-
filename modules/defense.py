import firebase_admin
from firebase_admin import firestore

class DefenseSystem:
    def __init__(self):
        self.db = firestore.client()
        # Reference to your reputation database
        self.reputation_ref = self.db.collection("security").document("reputation_list")
        self.status_ref = self.db.collection("security").document("system_status")

    def check_reputation(self, person_name):
        """Checks if a person is trusted based on Firebase data."""
        doc = self.reputation_ref.get()
        if doc.exists:
            data = doc.to_dict()
            # Get reputation score (0 to 100)
            score = data.get(person_name.lower(), 0) 
            
            if score >= 80:
                return f"Access Granted. Hello {person_name}. Reputation score: {score}."
            elif score >= 50:
                return f"Identity Verified. {person_name} is a known guest."
            else:
                return f"WARNING: {person_name} has a low reputation score. Monitoring active."
        return "Identity Unknown. Adding to observation log."

    def toggle_defense_mode(self, active=False):
        """Activates the 'Defense Mode' protocols."""
        status = "ACTIVE" if active else "OFF"
        self.status_ref.set({"defense_mode": status})
        
        if active:
            return "DEFENSE MODE ENGAGED. All security protocols are now live."
        else:
            return "Defense mode stand-down. Systems returning to normal."

    def add_new_person(self, name, initial_score=50):
        """Adds a new person to the reputation database."""
        self.reputation_ref.update({name.lower(): initial_score})
        return f"System updated. {name} has been indexed with a score of {initial_score}."

# --- Quick Test ---
if __name__ == "__main__":
    # This assumes Firebase is already initialized in your main.py
    defense = DefenseSystem()
    print(defense.check_reputation("Lakshay"))