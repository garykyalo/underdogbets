from datetime import datetime
import random 


def Daily_tip(match):
    confidence = random.uniform(80, 100)
    home_team, away_team = match['home_team'], match['away_team']
    league = match['league']
    odds = match['odds']
    time_str = match['time']
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
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
🎯 {home_team}  to win at odds <b> {odds[f'{home_team} win'][1]} 🎯</b>.

Stake: £10.

Platform: {odds[f'{home_team} win'][0]} → Go to Football > {league} > Match Result → Select {home_team}.
<i> Good luck!</i>
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




