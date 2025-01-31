### contains models that fetch data from endpoints not regularly updated
import requests
from ..config import settings
from sqlalchemy.orm import Session
from ..database import Bookmakers, Bettypes, Leagues

async def fetch_data(endpoint, params):
    sport="v3.football.api-sports.io"
    url = f"https://{sport}/{endpoint}"
    headers = {
  'x-rapidapi-key': settings.API_FOOTBALL,
  'x-rapidapi-host': sport
    }
    response = requests.request("GET", url, headers=headers,params=params)
    return response.json()

async def get_teams(db:Session):   ### call once a day 
    league_ids = [league_id[0] for league_id in 
                  db.query(Leagues.league_id).all() if league_id[0] is not None]
    endpoint = "teams"
    teams = []
    for league_id in league_ids:
        params = {"league": league_id, "season": 2024}
        league_teams = await fetch_data(endpoint, params)
        teams.append(league_teams)
    return teams 

async def get_betsandbookmakers(db:Session):
    items = {'bookmakers': Bookmakers, 'bets': Bettypes}
    params = {}
    for item in items:
        endpoint = f"/odds/{item}"
        data = await fetch_data(endpoint, params)
        bookmakers_data = data["response"]
        for bookmaker in bookmakers_data:
            if not bookmaker.get("id") or not bookmaker.get("name"):
                continue
            db.merge(items[item](id=bookmaker["id"], name=bookmaker["name"]))
    db.commit
    return "success"