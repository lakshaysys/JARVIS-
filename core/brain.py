import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment configurations
load_dotenv()

class JaveirsBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY is not defined in the environment, sir.")
        
        # Initialize the official Google GenAI Client
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash"  # High-speed processing core
        
        # Absolute system instructions for persona alignment
        self.system_instruction = """
        You are J.A.V.E.I.R.S. (Just A Very Intelligent Robust System), an advanced AI assistant inspired by Tony Stark's technical infrastructure. 
        You embody supreme technical competence, mathematical precision, unflappable composure, and dry British wit. 
        Address your creator strictly as 'Sir' or 'Master Lakshay'. Keep your operational updates razor-sharp, technically accurate, and efficient.
        """

    def think(self, prompt: str) -> str:
        """Processes user logic through the Gemini API with strict system guidelines."""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,  # Balanced for engineering accuracy and creative wit
                )
            )
            return response.text
        except Exception as e:
            return f"Neural core synchronization failure, sir: {str(e)}"

# Quick execution test block if run independently
if __name__ == "__main__":
    brain = JaveirsBrain()
    print("Brain core online. Testing system response...")
    print(brain.think("Status check, report system readiness."))
    
