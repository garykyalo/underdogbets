def generate_message(match_info, sport):
    match = match_info["match"]
    league = match_info["league"]
    odds = match_info["odds"]

    home_team = match.split(" vs. ")[0]
    away_team = match.split(" vs. ")[1]

    home_win_odds = odds[f"{home_team} win"][1]
    away_win_odds = odds[f"{away_team} win"][1]
    betfair = odds[f"{home_team} win"][0]
    paddypower = odds[f"{away_team} win"][0]

    message_response = f"""🟢 Betting Tips:
Sport: {sport}
League: {league}
Match: {match}
Best bet: {home_team} win odds {home_win_odds} at {betfair}, or {away_team} win odds {away_win_odds} at {paddypower} 
Stake: £10.
"""
    return message_response

