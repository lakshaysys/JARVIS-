import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env
load_dotenv()

# Verify required keys are present
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY is missing from environment variables, sir.", file=sys.stderr)
    sys.exit(1)

class JaveirsSystem:
    def __init__(self):
        print("Initializing J.A.V.E.I.R.S. core systems...")
        # Initialize the official Google GenAI client
        self.client = genai.Client(api_key=API_KEY)
        self.model_name = "gemini-1.5-flash"
        
        # Define the absolute operational system instructions
        self.system_instruction = """
        You are J.A.V.E.I.R.S. (Just A Very Intelligent Robust System), an advanced AI assistant inspired by Tony Stark's technical infrastructure. 
        You embody supreme technical competence, mathematical precision, unflappable composure, and dry British wit. 
        Address your creator exclusively as 'Sir' or 'Master Lakshay'. Provide concise status updates before deeper executions.
        """
        print("System online, Master Lakshay. All sensory channels active.")

    def process_command(self, user_query: str):
        """Sends user input through the Gemini client with system constraints."""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            return f"An anomaly occurred within the neural core, sir: {e}"

def main():
    jarvis = JaveirsSystem()
    print("\n-------------------------------------------------------------")
    print(" J.A.V.E.I.R.S. Interactive Terminal v2.6 (Secure Local Mode)")
    print(" Type 'exit' or 'quit' to terminate the session.")
    print("-------------------------------------------------------------")

    while True:
        try:
            user_input = input("\nMaster Lakshay > ")
            if not user_input.strip():
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("JARVIS: Shutting down secure links. Goodbye, sir.")
                break
            
            # Print status update in character
            print("JARVIS: Working on it now, sir...")
            response = jarvis.process_command(user_input)
            print(f"\nJARVIS:\n{response}")
            
        except KeyboardInterrupt:
            print("\nJARVIS: Emergency interrupt detected. Standing by, sir.")
            break

if __name__ == "__main__":
    main()
    
