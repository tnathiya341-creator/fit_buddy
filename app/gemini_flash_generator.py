import os
from dotenv import load_dotenv
load_dotenv()
KEY=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
MODEL=os.getenv("GEMINI_FLASH_MODEL","gemini-1.5-flash")
try:
    import google.generativeai as genai
    if KEY: genai.configure(api_key=KEY)
except ImportError: genai=None

def generate_nutrition_tip_with_flash(goal):
    fallback="Aim for balanced meals, adequate protein, vegetables or fruit, whole-food carbohydrate sources and regular hydration. Individual needs vary."
    if not genai or not KEY: return fallback
    try:
        p=f"Give one concise, general nutrition or recovery tip for the fitness goal: {goal}. Keep it practical and safe."
        return genai.GenerativeModel(MODEL).generate_content(p).text.strip()
    except Exception as e:
        print(e); return fallback
