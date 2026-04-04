import os
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import edge_tts
import pygame # Used for playing the generated voice

# --- 1. INITIALIZE FIREBASE ---
# Make sure your serviceAccountKey.json is in the config folder!
if not firebase_admin._apps:
    cred = credentials.Certificate("config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 2. INITIALIZE GEMINI ---
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

class JaveirsBrain:
    def __init__(self):
        self.name = "J.A.V.E.I.R.S."
        self.owner = "Lakshay Sherawat"
        self.memory_ref = db.collection("system").document("memory")
        self.defense_ref = db.collection("system").document("security")

    async def speak(self, text):
        """Converts text to a J.A.R.V.I.S. style British voice."""
        print(f"{self.name}: {text}")
        communicate = edge_tts.Communicate(text, "en-GB-RyanNeural")
        await communicate.save("speech.mp3")
        
        pygame.mixer.init()
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(1)
        pygame.mixer.quit()

    def get_context(self):
        """Retrieves past memory and security status from Firebase."""
        mem = self.memory_ref.get().to_dict() or {"history": []}
        sec = self.defense_ref.get().to_dict() or {"defense_mode": "OFF"}
        return mem["history"], sec["defense_mode"]

    def process_logic(self, user_input):
        """The thinking process."""
        history, defense_mode = self.get_context()
        
        # System instructions for the AI's personality
        prompt = (
            f"You are {self.name}, a robust AI built by {self.owner}. "
            f"Current Defense Mode: {defense_mode}. "
            f"Past context: {history[-3:]}. "
            f"User says: {user_input}"
        )
        
        response = model.generate_content(prompt)
        reply = response.text
        
        # Save to Firebase Memory
        history.append({"input": user_input, "output": reply})
        self.memory_ref.set({"history": history[-10:]}) # Keep last 10 lines
        
        return reply

    def toggle_defense(self, status):
        """Updates Defense Mode in Firebase."""
        self.defense_ref.update({"defense_mode": "ON" if status else "OFF"})
        return f"Defense mode is now {'activated' if status else 'deactivated'}."