import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class JaveirsBrain:
    def __init__(self):
        # This links J.A.V.E.I.R.S. to my Gemini 1.5 Flash brain
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-1.5-flash"

    def process_logic(self, user_input):
        """Sends your command to me to decide what to do."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_input
        )
        return response.text