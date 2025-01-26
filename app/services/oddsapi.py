import httpx, pandas as pd, json, random
from ..config import settings

base_url = "https://api.the-odds-api.com/v4/sports"

async def select_match():
    bestodds = await get_In_Season()
    match_ids = list(bestodds.keys())
    random_match_id = random.choice(match_ids)
    match = bestodds[random_match_id]
    return match


# fetch data from odds api
async def get_In_Season():
    params = {
        "apiKey": settings.ODDS_API_KEY,
        "all":True
      }
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        print("hii response", response, settings.ODDS_API_KEY)
        ## pick our specified list of leagues to check from
        with open('app/services/leagues.json', 'r') as file:
            target_leagues = json.load(file)
        df_target = pd.DataFrame(target_leagues)
        print("target DataFrame:", df_target.head())
        df_fetched = pd.DataFrame(response.json())
        print("Fetched DataFrame:", df_fetched.head())
        df_matched = pd.merge(df_fetched, df_target, on=['group','title'], how='inner')
        print("matched DataFrame:", df_matched.head())
        selected_leagues = json.loads(df_matched.to_json(orient='records'))
        bestodds = await get_odds_data(selected_leagues)
        return bestodds


## process the data to return a single match
async def get_best_odds(json_data):
    best_odds = {}
    for match in json_data:  
        match_id = match['id']
        home_team, away_team = match['home_team'], match['away_team']
        best_odds[match_id] = {
            'home_team': match['home_team'],
            'away_team':match['away_team'],
            'league':match["sport_title"], 
            'time': match['commence_time'],
            'odds': {}}

        for bookmaker in match['bookmakers']:
          
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    for outcome in market['outcomes']:
                        outcome_name = outcome['name']
                        odds = outcome['price']
                        key = f'{home_team} win' if outcome_name == home_team else f'{away_team} win' if outcome_name == away_team else 'draw'
                        
                        if key not in best_odds[match_id]['odds'] or odds > best_odds[match_id]['odds'][key][1]:
                            best_odds[match_id]['odds'][key] = (bookmaker['title'], odds)

    return best_odds


async def get_odds_data(selected_leagues):
    counter2 = 0
    bestodds = {}
    for item in selected_leagues:
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
                league_odds = await get_best_odds(data)
                bestodds.update(league_odds)
    return bestodds
