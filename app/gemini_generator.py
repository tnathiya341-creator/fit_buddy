import os
from dotenv import load_dotenv
load_dotenv()
KEY=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
MODEL=os.getenv("GEMINI_PRO_MODEL","gemini-1.5-pro")
try:
    import google.generativeai as genai
    if KEY: genai.configure(api_key=KEY)
except ImportError: genai=None

def fallback(goal, intensity):
    return f"""7-DAY {goal.upper()} PLAN - {intensity} INTENSITY
Day 1: Full body - warm-up, squats, push-up variation, glute bridges, cooldown.
Day 2: Cardio and mobility - comfortable cardio plus mobility work.
Day 3: Upper body - push/pull exercises and core, with recovery.
Day 4: Active recovery - easy movement and mobility.
Day 5: Lower body - squats/lunges or alternatives, glute and calf work.
Day 6: Cardio and core - moderate cardio and comfortable core exercises.
Day 7: Active recovery and stretching.
Adjust activity to your abilities and stop if exercise causes pain."""

def generate_workout_gemini(age, weight, goal, intensity):
    prompt=f"""Create a structured 7-day fitness plan.
Age: {age}; Weight: {weight} kg; Goal: {goal}; Intensity: {intensity}.
For each active day include a 5-10 minute warm-up, exercises with sets/reps or duration,
rest/recovery guidance and cooldown. Keep it practical and safe. Do not diagnose conditions."""
    if not genai or not KEY: return fallback(goal,intensity)
    try:
        return genai.GenerativeModel(MODEL).generate_content(prompt).text
    except Exception as e:
        print(e); return fallback(goal,intensity)
