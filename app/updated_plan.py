import os
from dotenv import load_dotenv
load_dotenv()
KEY=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
MODEL=os.getenv("GEMINI_PRO_MODEL","gemini-1.5-pro")
try:
    import google.generativeai as genai
    if KEY: genai.configure(api_key=KEY)
except ImportError: genai=None

def update_workout_plan(original_plan, feedback):
    if not genai or not KEY:
        return original_plan + "\n\nRequested update:\n" + feedback
    prompt=f"""Revise this 7-day workout plan according to the user's feedback.
ORIGINAL:
{original_plan}
FEEDBACK:
{feedback}
Return a complete revised plan. Keep it practical and safe."""
    try: return genai.GenerativeModel(MODEL).generate_content(prompt).text
    except Exception as e:
        print(e); return original_plan + "\n\nRequested update:\n" + feedback
