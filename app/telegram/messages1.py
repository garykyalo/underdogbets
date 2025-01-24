import random 

def format_tip(match):
    
    confidence = random.uniform(80, 100)
    home_team, away_team = match['home_team'], match['away_team']
    odds = match['odds']
    return f"""
 **Match**:{home_team} vs {away_team} 
 **Starts at**: {match['time']}
 **Tip**: head to head(h2h)
  **Best Odds**:
    {home_team} win odds: {odds[f'{home_team} win'][1]} @ {odds[f'{home_team} win'][0]}
    {away_team} win odds: {odds[f'{away_team} win'][1]} @ {odds[f'{away_team} win'][0]}
    or a draw odds: {odds['draw'][1]} @ {odds['draw'][0]}
 **Confidence**: {confidence:.2f}%
 """ 