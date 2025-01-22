from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..config import settings
import httpx
from .helper import get_odds_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.api_route("/", methods =["GET","POST"])
async def home (request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome"})

@router.get("/odds/{sport}")
async def get_odds(sport: str):
    result = await get_odds_data(sport)
    return result