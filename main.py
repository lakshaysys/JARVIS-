import asyncio
import speech_recognition as sr
from core.brain import JaveirsBrain

async def run_javeirs():
    brain = JaveirsBrain()
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    await brain.speak("Systems online. J.A.V.E.I.R.S. is ready for your command, Lakshay.")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio).lower()
            print(f"You: {query}")

            if "activate defense mode" in query:
                msg = brain.toggle_defense(True)
                await brain.speak(msg)
            
            elif "deactivate defense mode" in query:
                msg = brain.toggle_defense(False)
                await brain.speak(msg)

            elif "exit" in query or "shutdown" in query:
                await brain.speak("Powering down. Goodbye, Lakshay.")
                break

            else:
                response = brain.process_logic(query)
                await brain.speak(response)

        except Exception as e:
            print("Waiting for command...")

if __name__ == "__main__":
    asyncio.run(run_javeirs())