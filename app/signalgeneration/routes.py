from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .helper import get_odds_data
from .helpers2 import get_In_Season
from .helpers3 import extract_from_sportradar

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

router.mount("/static", StaticFiles(directory="app/static"), name="static")

@router.api_route("/", methods =["GET","POST"])
async def home (request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome"})

@router.get("/odds/{sport}")
async def get_odds(sport: str):
    result = await get_odds_data(sport)
   
   
    return result

@router.get("/leagues")
async def Leagues():
    #result = await get_In_Season()
    result = await extract_from_sportradar()
    return result