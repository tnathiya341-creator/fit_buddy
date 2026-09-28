from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///./fitbuddy.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    original_plan = Column(Text, nullable=False)
    nutrition_tip = Column(Text, nullable=False)
    updated_plan = Column(Text)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_user(user_id, username, age, weight, goal, intensity):
    db=SessionLocal()
    try:
        u=db.query(User).filter_by(user_id=user_id).first()
        if u:
            u.username, u.age, u.weight, u.goal, u.intensity = username, age, weight, goal, intensity
        else:
            u=User(user_id=user_id, username=username, age=age, weight=weight, goal=goal, intensity=intensity)
            db.add(u)
        db.commit()
        return u
    finally: db.close()

def save_plan(user_id, original_plan, nutrition_tip):
    db=SessionLocal()
    try:
        p=Plan(user_id=user_id, original_plan=original_plan, nutrition_tip=nutrition_tip)
        db.add(p); db.commit(); db.refresh(p); return p
    finally: db.close()

def get_user(user_id):
    db=SessionLocal()
    try: return db.query(User).filter_by(user_id=user_id).first()
    finally: db.close()

def get_original_plan(user_id):
    db=SessionLocal()
    try: return db.query(Plan).filter_by(user_id=user_id).order_by(Plan.id.desc()).first()
    finally: db.close()

def update_plan(user_id, updated_plan, feedback):
    db=SessionLocal()
    try:
        p=get_original_plan(user_id)
        if not p: return None
        p.updated_plan, p.feedback = updated_plan, feedback
        db.merge(p); db.commit(); return p
    finally: db.close()

def get_all_users():
    db=SessionLocal()
    try: return db.query(User).order_by(User.id.desc()).all()
    finally: db.close()

def get_all_plans():
    db=SessionLocal()
    try: return db.query(Plan).order_by(Plan.id.desc()).all()
    finally: db.close()
