## contains models  to store data into the database.
from sqlalchemy.orm import Session
from ..database import Teams, Fixtures, Prediction
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

async def store_predictions(db: Session, prediction):
    ("prediction record started")
    fixture_id = prediction["fixture"]
    predictions_data = str(prediction["predictions"])
    advice = prediction["advice"]
    bestodds= prediction["bestodds"]
    bookmaker = prediction["bookmaker"]
    existing_prediction = db.query(Prediction).filter_by(fixture_id=fixture_id).first()  
    if existing_prediction:
        existing_prediction.predictions_data = predictions_data
        existing_prediction.advice = advice
        existing_prediction.bet_odds= bestodds
        existing_prediction.bookmaker = bookmaker
    else:
        db.add(Prediction(
            fixture_id=fixture_id, 
            predictions_data=predictions_data,
            advice=advice,
            bet_odds= bestodds,
            bookmaker = bookmaker
            ))
    db.commit()
    print("prediction recorded")
    return "success"

