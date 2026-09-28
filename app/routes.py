from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from app.schemas import UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import save_user, save_plan, update_plan, get_original_plan, get_user, get_all_users, get_all_plans

router=APIRouter()
templates=Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@router.post("/generate-workout")
async def generate_workout(request: Request, username:str=Form(...), user_id:str=Form(...), age:int=Form(...), weight:float=Form(...), goal:str=Form(...), intensity:str=Form(...)):
    u=UserInput(username=username,user_id=user_id,age=age,weight=weight,goal=goal,intensity=intensity)
    plan=generate_workout_gemini(u.age,u.weight,u.goal,u.intensity)
    tip=generate_nutrition_tip_with_flash(u.goal)
    save_user(u.user_id,u.username,u.age,u.weight,u.goal,u.intensity)
    save_plan(u.user_id,plan,tip)
    return templates.TemplateResponse("result.html",{"request":request,**u.model_dump(),"workout_plan":plan,"nutrition_tip":tip,"updated_plan":None,"message":None})

@router.post("/submit-feedback")
async def submit_feedback(request:Request,user_id:str=Form(...),feedback:str=Form(...)):
    u=get_user(user_id); p=get_original_plan(user_id)
    if not u or not p: raise HTTPException(404,"User or plan not found")
    f=FeedbackRequest(user_id=user_id,feedback=feedback)
    updated=update_workout_plan(p.original_plan,f.feedback)
    update_plan(user_id,updated,f.feedback)
    return templates.TemplateResponse("result.html",{"request":request,"username":u.username,"user_id":u.user_id,"age":u.age,"weight":u.weight,"goal":u.goal,"intensity":u.intensity,"workout_plan":p.original_plan,"nutrition_tip":p.nutrition_tip,"updated_plan":updated,"message":"Your workout plan has been updated."})

@router.get("/view-all-users")
async def view_all_users(request:Request):
    users=get_all_users(); plans=get_all_plans()
    grouped={}
    for p in plans: grouped.setdefault(p.user_id,[]).append(p)
    return templates.TemplateResponse("all_users.html",{"request":request,"users":users,"plans_by_user":grouped})
