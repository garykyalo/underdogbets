from fastapi import APIRouter, Depends
from .config import settings
import  requests, json, os
from sqlalchemy.orm import Session
from .database import get_db, Leagues, Prediction, Fixtures, Bookmakers
from .services.fetchdata import get_fixtures, get_predictions
from .services.staticfetch import  get_bets, get_teams, fetch_data
from .services.telegram import send_image, send_message
from .services.messages import populate_message_data, Daily_tip, try_message
from .services.processodds import categorize_combo
router = APIRouter()


@router.get("/")
async def home():
    return "welcome to underdog tips"

@router.get("/leagues")
async def leagues(db: Session = Depends(get_db)):
    leagues = db.query(Leagues).all()
    pass



@router.get("/prediction")
async def prediction(db: Session = Depends(get_db)):
    #params = {"fixture": 1216195}
    #fetched_prediction = await fetch_data("predictions", params)
    prediction_fixtures = db.query(Fixtures).all()
    x = 0
    y= 0
    for fixture in prediction_fixtures:
        print("fixture", x)
        params = {"fixture": fixture.fixture_id}
        print(fixture.fixture_id)
        fetched_prediction = await fetch_data("predictions", params)
        if "response" not in fetched_prediction or not fetched_prediction["response"]:
            print(f"No prediction data found for fixture {fixture.fixture_id}. Skipping.")
            continue
        predictiondata = fetched_prediction["response"][0]["predictions"]
        fetched_odds = await fetch_data("odds", params)
        if "response" not in fetched_odds or not fetched_odds["response"]:
            print(f"No odds data found for fixture {fixture.fixture_id}. Skipping.")
            continue
        bookmakers = fetched_odds["response"][0]["bookmakers"]
        querybookmakers = db.query(Bookmakers).all()
        preferredbookmakers = [x.name for x in querybookmakers]
        print(preferredbookmakers, "hapa")
        highest_bet_dict = categorize_combo(predictiondata, fixture, bookmakers, preferredbookmakers)
        x += 1
        if  highest_bet_dict:
            odd = float(list(highest_bet_dict.values())[0])
            print("odd hapa:", odd)
            if odd >= 3:
                y += 1
                print("ndio hizi sasa hapa:", y)               
    return fetched_odds


@router.get("/basketball")
async def Basketball(db: Session = Depends(get_db)):
    endpoint = "teams"
    params = {"league": 95, "season":2024}
    data = await fetch_data(endpoint, params)
    return data

@router.get("/check")
def get (db: Session = Depends(get_db)):
    selected_prediction = db.query(Prediction).filter(
            Prediction.bet_odds >= 3 ).first()
    return selected_prediction

@router.get("/sendmessage")
async def SendMessage(db: Session = Depends(get_db)): 
    match = await populate_message_data(db)
    print (match, "hapa")
    fixtureid = match["fixture_id"]
    text = Daily_tip(match)
    imageurl = match["leaguelogo"]
    bookmaker = match["bookmaker"]
    bookmakerwebsite = match["website"]
    print(imageurl, "hapa")
    response = await send_message(db, text, fixtureid,bookmaker, bookmakerwebsite)
    return text

@router.get("/updatedata")
async def Updatedata(db: Session = Depends(get_db)):
    await get_teams(db)
    print("teams done")
    await get_bets(db)
    print("bets done")
    await get_fixtures(db)
    print("fixtures done")
    result = await get_predictions(db)
    print("predictions done")
    return result
    #return "successfully update all the tables"


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
    bookmakerpath = os.path.join(os.path.dirname(__file__), 'bookmakers.json')
    with open(bookmakerpath, 'r') as bookmaker:
        bookmakerdata = json.load(bookmaker)
    for item in bookmakerdata:
        new_bookmaker = Bookmakers(
            id = item.get('league_name'),
            name = item.get('bookmaker'),
            description= item.get('description'),
            website =item.get('website'))
        db.add(new_bookmaker)
    print("bookmakers done")
    db.commit()
    return {"message": "Leagues data inserted successfully"}