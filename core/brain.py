import os
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import speech_recognition as sr
import edge_tts

# 1. SETUP FIREBASE
# Ensure your serviceAccountKey.json is in the 'config/' folder
cred = credentials.Certificate("config/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. SETUP GEMINI AI
# Replace with your actual Gemini API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

class JarvisBrain:
    def __init__(self):
        self.name = "JARVIS"
        self.creator = "Lakshay Sherawat"
        self.chat_history_ref = db.collection("memory").document("chat_logs")
        
    def get_memory(self):
        """Fetches the last 5 messages from Firebase to give JARVIS context."""
        doc = self.chat_history_ref.get()
        if doc.exists:
            return doc.to_dict().get("history", [])
        return []

    def save_memory(self, user_input, jarvis_response):
        """Saves the conversation to Firebase."""
        history = self.get_memory()
        history.append({"user": user_input, "jarvis": jarvis_response})
        # Keep only the last 10 messages to save space
        self.chat_history_ref.set({"history": history[-10:]})

    async def speak(self, text):
        """Uses Edge-TTS for a natural British 'Jarvis' voice."""
        communicate = edge_tts.Communicate(text, "en-GB-RyanNeural")
        await communicate.save("output.mp3")
        os.system("start output.mp3") # Use 'afplay' on Mac or 'mpg123' on Linux

    def process_query(self, query):
        """Sends query to Gemini with personality and memory."""
        memory = self.get_memory()
        
        # System instructions to keep him in character
        system_prompt = f"Your name is {self.name}. You were created by {self.creator}. " \
                        f"Respond like a loyal, witty, and highly intelligent AI assistant. " \
                        f"Recent context: {memory}"
        
        response = model.generate_content(f"{system_prompt}\nUser: {query}")
        answer = response.text
        
        # Save to Firebase
        self.save_memory(query, answer)
        return answer

# --- MAIN EXECUTION LOOP ---
async def main():
    brain = JarvisBrain()
    recognizer = sr.Recognizer()
    
    print("JARVIS is online...")
    
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            
            try:
                user_text = recognizer.recognize_google(audio)
                print(f"You: {user_text}")
                
                if "exit" in user_text.lower() or "sleep" in user_text.lower():
                    await brain.speak("Going offline. Systems standing by.")
                    break
                
                # Get response from Brain
                reply = brain.process_query(user_text)
                print(f"JARVIS: {reply}")
                
                # Speak response
                await brain.speak(reply)
                
            except Exception as e:
                print("Could not understand or connection error.")

if __name__ == "__main__":
    asyncio.run(main())