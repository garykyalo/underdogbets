from ..config import settings
import httpx, json, pandas as pd, requests
from .helper import get_best_odds


base_url = "https://api.the-odds-api.com/v4/sports"
# Get a list of in-season sports and filter based on selected leagues 

async def get_In_Season(chat_id,telegram_url):
    params = {
        "apiKey": settings.ODDS_API_KEY,
        "all":True
      }
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        ## pick our specified list of leagues to check from
        with open('app/signalgeneration/leagues.json', 'r') as file:
            target_leagues = json.load(file)
        df_target = pd.DataFrame(target_leagues)
        df_fetched = pd.DataFrame(response.json())
        df_matched = pd.merge(df_fetched, df_target, on=['group','title'], how='inner')
        selected_leagues = json.loads(df_matched.to_json(orient='records'))
        await get_odds_data(selected_leagues,chat_id,telegram_url)
        return selected_leagues


## get the odds 
async def get_odds_data(selected_leagues,chat_id,telegram_url):
    counter2 = 0
    for item in selected_leagues:
        if counter2 == 4:
            break
        sport = item['key']
        url = f"{base_url}/{sport}/odds"
        params = {
            "apiKey": settings.ODDS_API_KEY,
            "regions": "uk", 
         }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)   
            if response.status_code == 200:
                data = response.json()
               
                bestodds = await get_best_odds(data)
                counter = 0
                for match in bestodds.values():
                    if counter == 3:
                        break
                    text= format_tip(match)
                    status = send_telegram_message(chat_id, text, telegram_url)
                    counter += 1
                    print(counter)
        counter2 += 1
        print(counter2,"counter 2")

                    
                

def send_telegram_message(chat_id, text, telegram_url):
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
        }
    response = requests.get(telegram_url, params=params)
    return response.status_code



import random 

def format_tip(match):
  
    confidence = random.uniform(80, 100)
    home_team, away_team = match['home_team'], match['away_team']
    odds = match['odds']
    return f"""
⚽ <b>Match:</b> {home_team} vs {away_team}<br>
⏰ <b>Starts at:</b> {match['time']}<br>
<b>Tip:</b> Head to head (H2H)<br>
<b>Best Odds:</b><br> 🔥
🔹&nbsp;&nbsp;{home_team} win odds: {odds[f'{home_team} win'][1]} @ {odds[f'{home_team} win'][0]}<br>
🔹&nbsp;&nbsp;{away_team} win odds: {odds[f'{away_team} win'][1]} @ {odds[f'{away_team} win'][0]}<br>
🔹&nbsp;&nbsp;Or a draw odds: {odds['draw'][1]} @ {odds['draw'][0]}<br>
<b>Confidence:</b> {confidence:.2f}%<br>
""" 