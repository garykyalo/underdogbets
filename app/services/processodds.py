import re
from collections import defaultdict

"""
we have 2 sets of data, prediction data and bookmakers.
from bookmakers we pick advice, winner and check if combo.
if combo we pick advice and calcualted combo odds, 
also get combo = true
Finally, the function return, bookmaker, odds, combo, match winner
"""
def extract_bets(predictiondata, fixture):
    print("here we are")
    advice = predictiondata['advice']
    winner_id = predictiondata['winner']['id']
    winner_mapping = {fixture.home_team: "Home", fixture.away_team: "Away"}
    winner = winner_mapping.get(winner_id)
    predictedbets = [{"bettype":"Match Winner", "value": winner}]
    if "Combo" in advice:
        print("its combo")
        bet2 = get_combo_bet(advice)
        predictedbets.append(bet2)
        print(predictedbets, "na hapa") 
    else:
        print("its not combo")
    return predictedbets

def categorize_combo(predictiondata, fixture, bookmakers,preferredbookmakers):
    predictedbets = extract_bets(predictiondata, fixture)
    if not predictedbets:
        return None
    for predictedbet in predictedbets:
        odds = categorize_predictions(predictedbet, bookmakers)
        predictedbet['odds'] = odds
    combopredictedbets =  calculate_combo_odds(predictedbets)
    print("ndio hizi hapa",combopredictedbets, "ndio hizi")
    print(preferredbookmakers, "prefered")
    print(combopredictedbets,"combo")
    highest_odd_bet_dict = find_highest_odds(combopredictedbets,preferredbookmakers)
    return highest_odd_bet_dict

def calculate_combo_odds(predictedbets):
    print(predictedbets, "here")
    combo_odds = {}
    match_odds = {odds["bookmaker"]: odds["value"] for odds in predictedbets[0]["odds"]}
    for bookmaker in match_odds.keys():
        if len(predictedbets) > 1:
            goal_odds = {odds["bookmaker"]: odds["value"] for odds in predictedbets[1]["odds"]}
            if bookmaker in goal_odds:
                combo_odds[bookmaker] =round((float(match_odds[bookmaker]) * float(goal_odds[bookmaker])), 2)
        else:
            combo_odds[bookmaker] = float(match_odds[bookmaker])
    return combo_odds

def get_combo_bet(advice):
    pattern = r"and\s+([\+\-]?(\d+\.\d+))"
    match = re.search(pattern, advice)
    if match:
        bet2 = match.group(1)
        value = match.group(2)
        bettype = "Goals Over/Under"
        betvalue = f"Over {value}" if "+" in bet2 else f"Under {value}"
        return {"bettype": bettype, "value": betvalue}
    return 

def find_highest_odds(combopredictedbets, preferredbookmakers):
    if not combopredictedbets:
        return {}
    preferred_odds = {k: v for k, v in combopredictedbets.items() if k in preferredbookmakers}
    if preferred_odds:
        highest_bookmaker = max(preferred_odds, key=preferred_odds.get)
        return {highest_bookmaker: preferred_odds[highest_bookmaker]}
    else:
        return "No preferred bookmaker found."
    
def categorize_predictions(predictedbet, bookmakers):
    print(predictedbet, "here we go")
    oddslist = []
    for bookmaker in bookmakers:
        bookmakername = bookmaker["name"]
        bets = bookmaker["bets"]
        for bet in bets:
            if bet["name"] == predictedbet["bettype"]:
                for item in bet["values"]:
                    if item["value"] == predictedbet["value"]:
                        oddslist.append({"bookmaker": bookmakername, "value": item["odd"]})
                        break
    return oddslist


'''
get odds, check if combo prediction. if not compbo prediction pass. 
if combo prediction, calculate odds, filter to only include where  calculated odds are greater than 3. 
'''