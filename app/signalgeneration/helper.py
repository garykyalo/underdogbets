from ..config import settings
import httpx

def get_best_odds(json_data):
    best_odds = {}

    for match in json_data:
        match_id = match['id']
        league = match["sport_title"]
        home_team, away_team = match['home_team'], match['away_team']
        best_odds[match_id] = {'match': f"{home_team} vs. {away_team}", 'league':league, 'time': match['commence_time'], 'odds': {}}

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


async def get_odds_data(sport: str):
    api_key = settings.ODDS_API_KEY
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": api_key,
        "regions": "uk",  
        "markets": "h2h" 
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)   
        if response.status_code == 200:
            data = response.json()
            result = get_best_odds(data)
            return result
        else:
            return {"error": "Failed to fetch odds"}
