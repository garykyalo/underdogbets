from fastapi import APIRouter, Request, Depends
from .config import settings
import requests, os, json
from sqlalchemy.orm import Session
from .database import get_db, Leagues
from .services.fetchdata import get_fixtures, get_odds, get_predictions
from .services.staticfetch import get_betsandbookmakers


router = APIRouter()


@router.get("/")
def home():
    return "Welcome to underdog tips, Here is home"

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



@router.get("/bookmakers")
async def Bookmakers(db: Session = Depends(get_db)):
    result = await get_betsandbookmakers (db)
    return result

@router.get("/prediction")
async def Prediction(db: Session = Depends(get_db)):
    result = await get_predictions(db)
    return result 


@router.get("/odds")
async def Odds(db: Session = Depends(get_db)):
    result = await get_odds(db)
    return result 


@router.get("/fixtures")
async def Fixtures(db: Session = Depends(get_db)):
    fixtures = await get_fixtures(db)
    return fixtures


### telegram routes 

@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    #response = await send_message(data)
    return data

@router.get("/set-webhook")
async def set_webhook():
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/setWebhook?url={settings.BASIC_URL}/webhook"
    response = requests.get(url)
    return response.json()

### insert data into the sql

@router.get("/checkleagues")
def check_league(db: Session = Depends(get_db)):
    query = db.query(Leagues).all()
    return {"leagues": query}

