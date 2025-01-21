from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..config import settings
import httpx


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.api_route("/", methods =["GET","POST"])
async def home (request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome"})

@router.get("/odds/{sport}")
async def get_odds(sport: str):
    api_key = settings.ODDS_API_KEY
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": api_key,
        "regions": "us",  
        "markets": "h2h" 
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)   
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch odds"}
        