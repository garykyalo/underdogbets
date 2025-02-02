from sqlalchemy.orm import Session
from ..database import Prediction, Fixtures, Teams, Leagues

async def populate_message_data(db:Session):
    selected_prediction = db.query(Prediction).filter(
        Prediction.message_send==False).first() 
    if not selected_prediction:
        print("No prediction found.")
        return {} 
    fixture_id = selected_prediction.fixture_id
    selected_fixture = db.query(Fixtures).filter(
        Fixtures.fixture_id == fixture_id).first()
    home_id =  selected_fixture.home_team
    away_id = selected_fixture.away_team
    league_id = selected_fixture.league_id
    print(league_id, fixture_id)
    hometeam = (db.query(Teams).filter(
        Teams.id == home_id).first()).team_name
    awayteam = (db.query(Teams).filter(
        Teams.id == away_id).first()).team_name
    league = db.query(Leagues).filter(
        Leagues.league_id == league_id).first()
    
    print(league, "hapa")
    response = {
        "fixture_id": fixture_id,
        "league": league.league_name,
        "leaguelogo": league.logo,
        "home_team": hometeam,
        "away_team": awayteam,
        "date": selected_fixture.date,
        "time": selected_fixture.time,
        "bet": selected_prediction.advice,
        "odds":selected_prediction.bet_odds,
        "bookmaker":selected_prediction.bookmaker
        }
    return response


def Daily_tip(match):
    return f"""
🟢 <b> Today’s Tips:</b> ⚽️  
Sport: Football 
League: {match['league']}
Match: <b> {match['home_team']} vs {match['away_team']} </b>
Date: {match['date']}
March Starts at: {match['time']}
💥 Bet: {match['bet']} at odds {match['odds']}
Stake: £10.

Platform: {match['bookmaker']} → Go to Football > {match['league']} > Match Result → {match['bet']}
<i> Good luck!</i> 😉 👍
"""

def weekly_stat():
    return f"""

<b>📊 Weekly Stats:</b>

    Total Tips: 15
    Wins: 12 ✅
    Losses: 3 ❌
    Profit: +24%.

<i>“ Keep winning with TheUnderdogTips ”</i>
"""




