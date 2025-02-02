from fastapi import APIRouter, Depends
from .config import settings
import  requests, json, os
from sqlalchemy.orm import Session
from .database import get_db, Leagues
from .services.fetchdata import get_fixtures, get_predictions
from .services.staticfetch import get_bookmakers, get_bets
from .services.staticfetch import get_teams
from fastapi.templating import Jinja2Templates
from .services.telegram import send_image
from .services.messages import populate_message_data, Daily_tip



router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home():
    return "Welcome to underdog tips, Here is home"


@router.get("/sendmessage")
async def SendMessage(db: Session = Depends(get_db)):
    match = await populate_message_data(db)
    fixtureid = match["fixture_id"]
    text = Daily_tip(match)
    imageurl = match["leaguelogo"]
    print(imageurl, "hapa")
    response = await send_image(db, text, imageurl, fixtureid)
    return response

@router.get("/updatedata")
async def Bookmakers(db: Session = Depends(get_db)):
    await get_teams(db)
    print("teams done")
    await get_bookmakers(db)
    print("bookmakers done")
    await get_bets(db)
    print("bets done")
    await get_fixtures(db)
    print("fixtures done")
    await get_predictions(db)
    print("predictions done")
    return "successfully update all the tables"


### telegram routes 
@router.get("/set-webhook")
async def set_webhook():
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/setWebhook?url={settings.BASIC_URL}/webhook"
    response = requests.get(url)
    return response.json()

### insert data into the sql
@router.get("/ourleagues")
async def Ourleagues(db: Session = Depends(get_db)):
    file_path = os.path.join(os.path.dirname(__file__), 'selected.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    for league in data:
        new_league = Leagues(
            league_name=league.get('league_name'),
            country=league.get('country'),
            sport=league.get('sport'),
            league_status=league.get('league_status'),
            logo=league.get('logo'),
            flag=league.get('flag'),
            league_id=league.get('league_id')
        )
        db.add(new_league)
    db.commit()
    return {"message": "Leagues data inserted successfully"}
