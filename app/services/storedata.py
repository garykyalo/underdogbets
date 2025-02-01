## contains models  to store data into the database.
from sqlalchemy.orm import Session
from ..database import Teams, Fixtures, Prediction, Odds
from datetime import datetime

async def store_teamsdata(db: Session, data):
    count = 1
    for item in data["response"]:
        team_data = item["team"]
            # Check if team already exists to avoid duplication
        existing_team = db.query(Teams).filter(Teams.id == team_data["id"]).first()
        if not existing_team:
            team = Teams(id=team_data["id"],
                team_name=team_data["name"],
                country=team_data["country"],
            code=team_data.get("code"),
            logo=team_data["logo"],)
            db.add(team)
            count +=1
            print(count)
    db.commit()
    return " teams succesfully added"


async def store_fixtures(db:Session, fixtures):
    x=1
    for item in fixtures:
        fixture_data = item["fixture"]
        league_data = item["league"]
        teams_data = item["teams"]
        date_str = datetime.strptime(fixture_data["date"], "%Y-%m-%dT%H:%M:%S%z")
        date = date_str.date()  # Outputs 'YYYY-MM-DD'
        time = date_str.time()
        existing_fixture = db.query(Fixtures).filter(Fixtures.fixture_id == fixture_data["id"]).first()
        if not existing_fixture:
            fixture = Fixtures(
                    fixture_id=fixture_data["id"],
                    time=time,
                    date=date,  
                    league_id=league_data["id"],
                    home_team=teams_data["home"]["id"],
                    away_team=teams_data["away"]["id"]
                )
            db.add(fixture)
            x += 1
            print(x)
    db.commit()
    return "success"

async def store_predictions(db: Session, predictions):
    for prediction in predictions:
        fixture_id = prediction["fixture"]
        predictions_data = str(prediction["predictions"])
        advice = prediction["advice"]
        existing_prediction = db.query(Prediction).filter_by(fixture_id=fixture_id).first()  
        if existing_prediction:
            existing_prediction.predictions_data = predictions_data
            existing_prediction.advice = advice
        else:
            db.add(Prediction(fixture_id=fixture_id, predictions_data=predictions_data, advice=advice))
    db.commit()
    return "success"

async def store_odds(db: Session, odds):               
    for odds_data in odds:
        print(2)
        fixture_id = odds_data["fixture"]["id"]
        update_time = odds_data["update"]
        bookmakers = str(odds_data["bookmakers"])
        existing_odds = db.query(Odds).filter(Odds.fixture_id == fixture_id).first()
        
        if existing_odds:
            # Update the existing odds if data has changed
            existing_odds.update_time = update_time
            existing_odds.bookmakers = bookmakers
        else:
            # Create a new odds record
            new_odds = Odds(
                fixture_id=fixture_id,
                name=odds_data["league"]["name"],
                league_id=odds_data["league"]["id"],
                update_time=update_time,
                bookmakers=bookmakers
            )
            db.add(new_odds)
    db.commit()
    return "success"