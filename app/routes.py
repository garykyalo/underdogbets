from fastapi import APIRouter, Request, Depends
from .config import settings
import requests, os, json
from sqlalchemy.orm import Session
from .database import get_db, Leagues
from .services.fetchdata import get_fixtures, get_odds, get_predictions
from .services.staticfetch import get_bookmakers, get_bets
from .services.storedata import store_teamsdata
from .services.staticfetch import get_teams
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .gptmodel import get_openai_response, generate_odds
from .database import Fixtures, Prediction, Odds
from datetime import date
router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home():
    return "Welcome to underdog tips, Here is home"

@router.get("/bestodds")
async def bestodds(db: Session = Depends(get_db)):
    response = await generate_odds(db)
    print(response)
    return response



@router.get("/fixtures")
def fixtures(db: Session = Depends(get_db)):
    #query = db.query(Fixtures).filter(Fixtures.date == date.today()).all()
    query = db.query(Fixtures).filter(Fixtures.fixture_id ==1293561).first()
    return {"fixtures": query}

@router.get("/prediction")
def prediction(db: Session = Depends(get_db)):
    #query = db.query(Prediction).all()
    query = db.query(Prediction).filter(Prediction.fixture_id ==1293561).first()
    return {"prediction": query}

@router.get("/odds")
def OddsQuery(db: Session = Depends(get_db)):
    #query = db.query(Odds).all()
    query = db.query(Odds).filter(Odds.fixture_id ==1293561).first()
    return {"odds": query}

@router.api_route("/chat", methods=["GET", "POST"], response_class=HTMLResponse)
async def chat(request: Request):
    if request.method == "POST":
        form_data = await request.form()
        prompt = form_data.get("prompt")
        openai_response = await get_openai_response(prompt)
    else:
        prompt = None
        openai_response = None
    return templates.TemplateResponse("index.html", {
        "request": request,
        "openai_response": openai_response,
        "prompt": prompt
    })



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
    await get_odds(db)
    print("odds done")
    return "successfully update all the tables"


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
