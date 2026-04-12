import asyncio
import speech_recognition as sr
# Corrected Imports
from core.brain import JaveirsBrain
from modules.vision import JaveirsVision
from modules.defense import DefenseSystem

async def run_javeirs():
    # Initialize the systems
    brain = JaveirsBrain()
    vision = JaveirsVision()
    security = DefenseSystem()
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Startup Greeting
    await brain.speak("Systems online. J.A.V.E.I.R.S. is ready for your command, Lakshay.")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("\nListening...")
            try:
                # Set a timeout so it doesn't wait forever if you aren't talking
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                continue

        try:
            print("Processing...")
            query = recognizer.recognize_google(audio).lower()
            print(f"You: {query}")

            # 1. Defense Mode Commands
            if "activate defense mode" in query:
                msg = security.toggle_defense_mode(True)
                await brain.speak(msg)
            
            elif "deactivate defense mode" in query:
                msg = security.toggle_defense_mode(False)
                await brain.speak(msg)

            # 2. Vision / Scanning Commands
            elif "scan" in query or "identify" in query:
                await brain.speak("Initializing optical sensors. Scanning now.")
                scan_result = vision.scan_and_read()
                await brain.speak(scan_result)

            # 3. Shutdown Command
            elif "exit" in query or "shutdown" in query or "sleep" in query:
                await brain.speak("Powering down all systems. Goodbye, Lakshay.")
                break

            # 4. General AI Conversation
            else:
                response = brain.process_logic(query)
                await brain.speak(response)

        except sr.UnknownValueError:
            # This happens if it hears noise but no words
            pass
        except Exception as e:
            print(f"System Note: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_javeirs())
    except KeyboardInterrupt:
        print("\nManual override: J.A.V.E.I.R.S. offline.")