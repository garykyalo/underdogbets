from sqlalchemy.orm import Session
from ..database import Prediction, Fixtures, Teams, Leagues, Bookmakers
from datetime import datetime, timedelta

async def populate_message_data(db:Session):
    while True:
        #predictions = db.query(Prediction).filter(Prediction.message_send == False,
        #   Prediction.bet_odds >= 2.5).all()
        prediction = db.query(Prediction).filter(Prediction.message_send == False).order_by(Prediction.bet_odds.desc()).first()
        '''if not predictions:
            print("No prediction found.")
            return {}
        fixture_ids = [fixture.fixture_id for fixture in predictions]
        selected_fixture = db.query(Fixtures).filter(Fixtures.fixture_id.in_'
        (fixture_ids)).order_by(Fixtures.date.asc()).first()'''
        selected_fixture = db.query(Fixtures).filter(Fixtures.fixture_id == prediction.fixture_id).first()
        match_time = selected_fixture.time
        match_date = selected_fixture.date
        match_datetime = datetime.combine(match_date, match_time)
        timenow = datetime.now()
        selected_prediction = db.query(Prediction).filter(Prediction.fixture_id == selected_fixture.fixture_id).first()
        if match_datetime > timenow:
            print(f"Upcoming match: {selected_fixture}")
            print(selected_fixture.time)
            break
        else:
            print("Match has already passed, marking the prediction as processed...")
            print(selected_fixture.time)
            selected_prediction.message_send = True
            db.commit() 
            continue  
 
    home_id =  selected_fixture.home_team
    away_id = selected_fixture.away_team
    league_id = selected_fixture.league_id
    hometeam = db.query(Teams).filter(
        Teams.id == home_id).first().team_name
    print(hometeam)
    awayteam = db.query(Teams).filter(
        Teams.id == away_id).first().team_name
    league = db.query(Leagues).filter(
        Leagues.league_id == league_id).first()
    bookmakerwebsite = (db.query(Bookmakers).filter(
        Bookmakers.name == selected_prediction.bookmaker).first()).website
    
    print(league, "hapa")
    response = {
        "fixture_id": selected_fixture.fixture_id,
        "league": league.league_name,
        "leaguelogo": league.logo,
        "home_team": hometeam,
        "away_team": awayteam,
        "date": selected_fixture.date,
        "time": selected_fixture.time,
        "bet": selected_prediction.advice,
        "odds":selected_prediction.bet_odds,
        "bookmaker":selected_prediction.bookmaker,
        "website": bookmakerwebsite
        }
    return response

def try_message(match):
    date_obj = match["date"]
    date = date_obj.strftime("%A, %d %B %Y")
    time = match["time"]
    
    print(time)
    return f"""

    ❗️ Daily BET from Tip ❗️
⚽️ Football - {match['league']}

<b>{match['home_team']} vs {match['away_team']} </b>

🎯 Tip: {match['bet']} 
💰 Best Odds:{match['odds']} @ {match['bookmaker']}

⏰ Gamesstart at {time} (UTC)
📅  {date}
Stake: £10.
<i> Good luck!</i> 😉 👍
"""


def Daily_tip(match):
    odds = float(match['odds'])
    stake = round(10, 2)
    payout = round(stake * odds, 2)
    profit = round(payout - stake, 2)
    return f"""
🟢‼️ <b> Today’s Tips:</b> ⚽️   
Sport: Football 
League: {match['league']}
Match: <b> {match['home_team']} vs {match['away_team']} </b>
📆 Date: <b> {match['date']} </b>
⏰ March Starts at: {match['time']}
💥 Bet: {match['bet']} at odds {match['odds']}
💸 Stake: £ {stake}.
🏆 Potential Payout: £ {payout}
🎯 Net Profit: £ {profit}

Step by step guide📝

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




