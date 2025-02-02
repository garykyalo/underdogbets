### contains models that fethc data  regularly
from .staticfetch import fetch_data
from .storedata import store_fixtures, store_predictions
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database import Leagues, Fixtures
import asyncio
from .processodds import categorize_combo

async def get_fixtures(db:Session):              #call every hour
    print("called")
    date_list = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    endpoint = "fixtures"
    league_ids = [league_id[0] for league_id in db.query(Leagues.league_id).all() if league_id[0] is not None]
    new_fixtures = []
    for date in date_list:
        params = {"date": date}
        fetched_fixtures = await fetch_data(endpoint, params)
        await asyncio.sleep(1)
        for item in fetched_fixtures["response"]:
            if item["league"]["id"] in league_ids:
                new_fixtures.append(item)
    result = await store_fixtures(db,new_fixtures)
    return new_fixtures


async def get_predictions(db:Session):                      ### one call per hour 
    todays_fixtures = db.query(Fixtures).filter(
       Fixtures.date == datetime.now().date()).all()
    x = 0
    for fixture in todays_fixtures:
        params = {"fixture": fixture.fixture_id}
        fetched_prediction = await fetch_data("predictions", params)
        bet_advice = fetched_prediction["response"][0]["predictions"]["advice"]
        response = fetched_prediction["response"][0]["predictions"]
    

        fetched_odds = await fetch_data("odds", params)
        if "response" not in fetched_odds or not fetched_odds["response"]:
            print(f"No odds data found for fixture {fixture.fixture_id}. Skipping.")
            continue
        bookmakers = fetched_odds["response"][0]["bookmakers"]
        highest_odd_bet_dict = categorize_combo(response, fixture, bookmakers)
        result = {
            "fixture": fixture.fixture_id,
            "predictions": fetched_prediction["response"][0]["predictions"],
            "advice": bet_advice,
            "bookmaker":  highest_odd_bet_dict["bookmaker"],
            "bestodds":  highest_odd_bet_dict["odd"]
            }
        x += 1
        print("prediction", x)
        storedata = await store_predictions(db, result)
        await asyncio.sleep(3)
    return result
