import asyncio
import os
import speech_recognition as sr
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Import your custom modules
from core.brain import JaveirsBrain
from modules.vision import JaveirsVision
from modules.defense import DefenseSystem

# Load API keys from .env
load_dotenv()

async def run_javeirs():
    print("--- STARTING J.A.V.E.I.R.S. CORE ---")

    # 1. INITIALIZE FIREBASE (Must happen before DefenseSystem)
    if not firebase_admin._apps:
        try:
            # Ensure this file exists in your config folder!
            cred = credentials.Certificate("config/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            print("[System] Firebase connection established.")
        except Exception as e:
            print(f"[Fatal Error] Could not initialize Firebase: {e}")
            return

    # 2. INITIALIZE CORE MODULES
    try:
        brain = JaveirsBrain()
        vision = JaveirsVision()
        security = DefenseSystem()
        
        recognizer = sr.Recognizer()
        # Note: This requires PyAudio to be installed via dev.nix
        mic = sr.Microphone()
        
        print("[System] All hardware modules linked.")
    except Exception as e:
        print(f"[Fatal Error] Module initialization failed: {e}")
        return

    # 3. STARTUP GREETING
    startup_msg = "Systems online. I am ready for your command, Master Lakshay."
    print(f"J.A.V.E.I.R.S.: {startup_msg}")
    # await brain.speak(startup_msg) # Uncomment if you have edge-tts ready

    # 4. MAIN COMMAND LOOP
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("\n[Listening...]")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                continue

        try:
            # Convert speech to text
            query = recognizer.recognize_google(audio).lower()
            print(f"Lakshay: {query}")

            # COMMAND: Defense Protocols
            if "activate defense mode" in query:
                status = security.toggle_defense_mode(True)
                print(f"J.A.V.E.I.R.S.: {status}")
            
            # COMMAND: Optical Scanning
            elif "scan environment" in query or "identify" in query:
                print("J.A.V.E.I.R.S.: Initiating optical sensors...")
                result = vision.scan_and_read()
                print(f"J.A.V.E.I.R.S.: {result}")

            # COMMAND: System Exit
            elif "shutdown" in query or "goodbye" in query:
                print("J.A.V.E.I.R.S.: Powering down. Security protocols remain active.")
                break

            # DEFAULT: Artificial Intelligence Logic (Gemini)
            else:
                reply = brain.process_logic(query)
                print(f"J.A.V.E.I.R.S.: {reply}")

        except sr.UnknownValueError:
            # This happens if it hears noise but no clear words
            pass 
        except Exception as e:
            print(f"[Runtime Error]: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_javeirs())
    except KeyboardInterrupt:
        print("\n[Manual Override] J.A.V.E.I.R.S. Offline.")