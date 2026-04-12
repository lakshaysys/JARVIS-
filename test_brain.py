import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    response = model.generate_content("Javeirs, are you online?")
    print("Response from J.A.V.E.I.R.S.:", response.text)
    print("\n✅ API Key is working perfectly!")
except Exception as e:
    print(f"❌ Error: {e}")