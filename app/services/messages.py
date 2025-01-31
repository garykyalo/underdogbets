from datetime import datetime



def Daily_tip(match):
    home_team, away_team = match['home_team'], match['away_team']
    league = match['league']
    time_str = match['time']
    bookmaker_name= match['bookmaker_name']
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M (UTC)")
    return f"""
🟢 <b> Today’s Tips:</b>
Sport: Football ⚽️ 
League: {league}
Match: <b> {home_team} vs {away_team} </b>
Date: {date}
March Starts at: {time}
💥 Bet:
🎯<b> {match['bet_outcome']} for {match['bet_name']}, odds {match['odds']}🎯</b>.

Stake: £10.

Platform:{bookmaker_name} → Go to Football > {league} > Match Result →
 Select: <b> {match['bet_outcome']} for {match['bet_name']}.</b>
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




