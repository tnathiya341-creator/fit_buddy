# FitBuddy AI

FastAPI + Jinja2 + SQLAlchemy/SQLite + Gemini implementation based on the supplied FitBuddy document.

Features:
- Personalized 7-day workout generation
- Nutrition/recovery tip
- Feedback-based plan updating
- SQLite persistence
- Admin/coach view
- FastAPI /docs

Run:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Copy .env.example to .env and add your Gemini API key.

Start:
uvicorn app.main:app --reload

Open http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs
