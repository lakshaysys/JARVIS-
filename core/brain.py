import os
from dotenv import load_dotenv
from google import genai # New import

load_dotenv()

class JaveirsBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        # Initialize the new Client
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-1.5-flash"

    def process_logic(self, query):
        """Sends user input to the cloud brain."""
        response = self.client.models.generate_content(
            model=self.model_id, 
            contents=query
        )
        return response.text