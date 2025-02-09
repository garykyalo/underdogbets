### contains models that fethc data  regularly
from .staticfetch import fetch_data
from .storedata import store_fixtures, store_predictions
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database import Leagues, Fixtures, Bookmakers
import asyncio
from .processodds import categorize_combo, get_combo_bet

async def get_fixtures(db:Session):              #call every hour
    print("called")
    date_list = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(2)]
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
    #today = datetime.now().date()
    #tomorrow = today + timedelta(days=3)
    #prediction_fixtures = db.query(Fixtures).filter(
    #    Fixtures.date.in_([today, tomorrow])).all()
    prediction_fixtures = db.query(Fixtures).all()
    print("hapa 1", prediction_fixtures)
    x = 0
    querybookmakers = db.query(Bookmakers).all()
    print("hapa 2", querybookmakers)
    preferredbookmakers = [x.name for x in querybookmakers]
    fetched_oddslist = []
    for fixture in prediction_fixtures:
        params = {"fixture": fixture.fixture_id}
        print("hapa 4", params)
        fetched_prediction = await fetch_data("predictions", params)
        print("hapa 5", fetched_prediction)
        bet_advice = fetched_prediction["response"][0]["predictions"]["advice"]
        print("hapa 6", bet_advice)
        winner = fetched_prediction["response"][0]["predictions"]["winner"]["name"]
        print("hapa 7", winner)
        if "Combo" in bet_advice:
            bettype = get_combo_bet(bet_advice)
            advice = f"Combo: {winner} to win & over {bettype}"
        else:
            advice = f"{winner} to win"
        response = fetched_prediction["response"][0]["predictions"]
        print("hapa 8", response)
        fetched_odds = await fetch_data("odds", params)
        fetched_oddslist.append(fetched_odds)
        print("hapa 9", fetched_odds)
        if "response" not in fetched_odds or not fetched_odds["response"]:
            print(f"No odds data found for fixture {fixture.fixture_id}. Skipping.")
            continue
        bookmakers = fetched_odds["response"][0]["bookmakers"]
        print("hapa 10", bookmakers)

        highest_odd_bet_dict = categorize_combo(response, fixture, bookmakers, preferredbookmakers)
        print("hapa 11", highest_odd_bet_dict)
        for bookmaker, odds in highest_odd_bet_dict.items():
            bookmakername = bookmaker
            bookmakerodds = odds
        result = {
            "fixture": fixture.fixture_id,
            "predictions": fetched_prediction["response"][0]["predictions"],
            "advice": advice,
            "bookmaker":  bookmakername,
            "bestodds":  bookmakerodds
            }
        x += 1
        print("prediction", x)
        storedata = await store_predictions(db, result)
        await asyncio.sleep(3)
    return fetched_oddslist
