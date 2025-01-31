### contains models that fethc data  regularly
from .staticfetch import fetch_data
from .storedata import store_fixtures, store_predictions, store_odds
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database import Leagues, Fixtures


async def get_fixtures(db:Session):              #call every hour
    """"
    fetch fixtures from fixtures endpoint (use a loop to fetch 3 days)
    filter the fictures based on our leagues
     record the filtered fixures into fixtures table
    """
    date_list = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    endpoint = "fixtures"
    league_ids = [league_id[0] for league_id in db.query(Leagues.league_id).all() if league_id[0] is not None]
    new_fixtures = []
    for date in date_list:
        params = {"date": date}
        fetched_fixtures = await fetch_data(endpoint, params)
        for item in fetched_fixtures["response"]:
            if item["league"]["id"] in league_ids:
                new_fixtures.append(item)
    result = await store_fixtures(db,new_fixtures)
    return new_fixtures


async def get_predictions(db:Session):                      ### one call per hour 
    """
    fetch predictions from the predictions endpoint
    filter by fixture id from the fixtures table
    store them to predictions table, ensure any that needs update is updated. 
    no duplicate fixtures.
    """
    endpoint = "predictions"
    todays_fixtures = db.query(Fixtures).filter(
        Fixtures.date == datetime.now().date()).all()
    predictions = []
    for fixture in todays_fixtures:
        params = {"fixture": fixture.fixture_id}
        data = await fetch_data(endpoint, params)
        result = {
            "fixture": fixture.fixture_id,
            "predictions": data["response"][0]["predictions"],
            "advice": data["response"][0]["predictions"]["advice"]
            }
        predictions.append(result)
    result = await store_predictions(db,predictions)
    return predictions

async def get_odds(db:Session):   #### one call every 3hrs
    """
    use todays fixtures, id to get odds from the odds endpoint
    use todays fixtures, to get todays predictions for the same odds
    record them into the oodds table.
    for each fixture, and  best odd, loop over the bookmakers  to select the highest odd
    add a function to calculate odds for combo ( combo is just a list of bets so the function can be used  even for non-combo, list with one item) 
    """
    todays_fixtures = db.query(Fixtures).filter(
        Fixtures.date == datetime.now().date()).all()
    endpoint = "odds"
    odds = []
    for fixture in todays_fixtures:
        params = {"fixture": fixture.fixture_id}
        data = await fetch_data(endpoint, params)
        oddsresponse = odds["response"]
        odds.append(oddsresponse)
    result = store_odds(db, oddsresponse)
    return odds

    ## we need to figure out  how the advice from the prediction can translate to a list of odds. 
    ## return the dictionery for message formulation. 