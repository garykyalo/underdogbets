import requests, random
from datetime import datetime, timedelta
from ..config import settings 
from sqlalchemy.orm import Session
from ..database import Leagues, Fixtures, Teams

football = "v3.football.api-sports.io"
baskteball = "v1.basketball.api-sports.io"

headers = {
    'x-rapidapi-host': "v1.basketball.api-sports.io",
    'x-rapidapi-key': "XxXxXxXxXxXxXxXxXxXxXxXx"
    }

 #endpoint = "odds/bookmakers"    ## gives a list of bookmakers, updated daily
    #endpoint = "/odds?date=2025-01-31"   ## gives odds for prematch updated every 3 hrs
    #endpoint = "/odds/mapping"           ## gives a list of available fixtures id, used in odds endpoint
    #endpoint = "teams"
    #endpoint = "leagues" # gives a list of all leagues and league ids, do not change

async def fetch_data(endpoint, params, sport= football): 
    url = f"https://{sport}/{endpoint}"
    headers = {
  'x-rapidapi-key': settings.API_FOOTBALL,
  'x-rapidapi-host': sport
    }
    response = requests.request("GET", url, headers=headers,params=params)
    return response.json()



async def Get_todays_odds(db:Session):
    date_list = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    endpoint = "odds"
    todays_fixtures = db.query(Fixtures).filter(Fixtures.date == date.today()).all()
    
    fixture_ids = [fixture.fixture_id for fixture in todays_fixtures]
    print(fixture_ids, "hapa")
    filtered_odds=[]
    for date in date_list:
        params = {
        "date": date}
        requested_odds = await fetch_data(endpoint, params, sport= football)
        day_odds = [odds for odds in requested_odds["response"] if odds["fixture"]["id"] in fixture_ids]
        filtered_odds.extend(day_odds)
    selected_bet = random_bet_selection(filtered_odds)
    result = populate_message_data(db, selected_bet, todays_fixtures)
    return filtered_odds


def random_bet_selection(filtered_odds):
    result = []
    for odds in filtered_odds:
        fixture_id = odds["fixture"]["id"]
        # Select a random bookmaker
        selected_bookmaker = random.choice(odds["bookmakers"])
        bookmaker_id = selected_bookmaker["id"]
        bookmaker_name = selected_bookmaker["name"]
        # Select a random bet from the bookmaker
        selected_bet = random.choice(selected_bookmaker["bets"])
        bet_id = selected_bet["id"]
        bet_name = selected_bet["name"]
        
        # Select a random value from the bet values (e.g., "Home", "Away", "Draw")
        selected_bet_value = random.choice(selected_bet["values"])
        bet_value = selected_bet_value["value"]
        odds_value = selected_bet_value["odd"]
        
        # Create the dictionary with the required keys
        result.append({
            "fixture_id": fixture_id,
            "bookmaker_id": bookmaker_id,
            "bookmaker_name": bookmaker_name,
            "bet_id": bet_id,
            "bet_name": bet_name,
            "bet_outcome": bet_value,   # This is the random bet value (e.g., "Home", "Away", "Draw")
            "odds": odds_value        # The odds corresponding to the selected bet value
        })
    selected_bet = random.choice(result)
    # Return the result after processing all the odds
    return selected_bet

def populate_message_data(db: Session, selected_bet, todays_fixtures):
  ## we need, odds, league,  hometeam,awayteam, date, time,
  selected_fixture_id = selected_bet["fixture_id"]
  selected_fixture = next(fixture for fixture in todays_fixtures if fixture.fixture_id == selected_fixture_id)
  league = (db.query(Leagues).filter(Leagues.league_id == selected_fixture.league_id).first()).league_name
  date = selected_fixture.date
  time = selected_fixture.time
  home_team = (db.query(Teams).filter(Teams.id == selected_fixture.home_team).first()).team_name
  away_team = (db.query(Teams).filter(Teams.id == selected_fixture.away_team).first()).team_name
  selected_bet.update({
        "league": league,
        "date": date,
        "time": time,
        "home_team": home_team,
        "away_team": away_team
    })
  return selected_bet
  



### steps to pick the data 
""""
1. get  the selected leagues from the database( leagues table)
2. filter for  the ones on seasons, and return their league Ids. 
Should be a list of league Ids you can loop over. 

>> u get the fixtures for each day
>> check if there are any fixtures for our selected leagues
>> pick  the fixture details(fixture id, teams(home and away: id), time ) >> store this into a database

++ check predictions and pick the best prediction for each fixture
++ check if combo:
    >> get a list of betting options for the combo, if not combo the list will contain one item
++ get the prediction percentage
    >use the prediction to determine the betting option or options if combo.
    >use the betting option to get the best odds from the best bookmaker

>> move to odds, use the ficture id from fictures, get the best odds from the best bookmaker. 

### 

3. use the list of league ids to get fixtures, for the last season. 

4. filter the fixtures by date( return the ones due today), fixture ids.

"""

"""
STEPS 
1. get a list of bookmakers
2. get a list of all available betting options
3. build models to connect predicted bet option to available options and best bookmaker and best odds
"""

"""
STEP 3:: BUILD PREDICTION LOGIC

>> understand how gpt works, build a small app that picks  input and returns output.
>> instruct the model to pick output from my database()
    ++ give it inputs( todays fixtures)
    +++ produce output predictions,and best bookmaker together with its odds
    +++ use that output to combile a message
>> ensure the bot can send both  plain text and images.

"""

"""
model process 
get a fixture, fixtureid,
++ use that fixtureid to get predictions, 
++ send the prediction to chatpt to split it into data that odds can understand
++ use that data to retrieve the best odds, best bookmaker

>> write a prompt with prediction and odds >> loop over for each fixture
>> return highest odds bookmaker, list [{betname, odds}, {betname2, odds2}] *** just prompt to return a structured message****
+++ have a different prompt for a combo, 
+++ re
"""

### example messsage output Bet: Combo Double Chance (Deportivo W or Draw) + Under 3.5 Goals
############################# odds 
""""

based on the following prediction:
{insert prediction}
iterate over the following odds and return the  bookmaker with the highest odds.
{insert odds }
format the response as, 
bookmaker: <bookmaker>
bet:<bet advice>
odds:<odds from the selected bookmaker>

"""


""""
How to populate  message data
1. query the predictions table, for fixtures where message sent is not true
    >>  here we get fixtureids, advice,bestbookmaker, bestodds
2. fetch fixtures on on all today fixtures
    ++ randomly select one
    >> here we get time, date,
    >> carry through league id, team ids( home and away)
3.  fetch league name fro leagues table based on league ID
4. fetch team names from tems table based on tema Id
**** Hooray Now send the message**** 
"""