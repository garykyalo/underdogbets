import re 

def categorize_combo(predictiondata, fixture,bookmakers):
    """
    if combo loop over the categorise prediction, provide a list of odds for each  specific category. 
    calculate combo odds and then pick the highest. 

    """
    predictedbets = extract_bet(predictiondata, fixture)
    oddslist = []
    for predictedbet in predictedbets:
        oddslistitem = categorize_predictions(predictedbet, bookmakers)  #### add logic to calculate combo odds
        oddslist.append(oddslistitem)
        highest_odd_bet = max(oddslistitem, key=lambda x: float(x["value"]))
        highest_odd_bet_dict = {"bookmaker": highest_odd_bet["bookmaker"], "odd": highest_odd_bet["value"]}
    return highest_odd_bet_dict

def extract_bet(predictiondata, fixture):
    advice = predictiondata['advice']
    winner_id = predictiondata['winner']['id']

    winner_mapping = {fixture.home_team: "Home", fixture.away_team: "Away"}
    bettype = "Double Chance" if predictiondata['win_or_draw'] else "Match Winner"
    winner = winner_mapping.get(winner_id, None)
    value_mapping = {
    "Double Chance": "Home/Draw" if winner == "Home" else "Draw/Away" if winner == "Away" else winner,
    "Match Winner": winner
    }
    value = value_mapping.get(bettype, None)
    predictedbet = [{"bettype": bettype, "value": value}]
    combo = True if "Combo" in advice  else False
    if combo:
        pattern = r"and\s+([\+\-]?(\d+\.\d+))"
        match = re.search(pattern, advice)
        if match:
            bet2 = match.group(1)
            value = match.group(2) 
            bettype = "Goals Over/Under"
            betvalue = f"Over {value}" if "+" in bet2 else f"Under {value}"
            predictedbet2 = {"bettype": bettype, "value": betvalue}
            predictedbet.append(predictedbet2)
    return predictedbet



def calculateComboOdds():
    pass

def categorize_predictions(predictedbet, bookmakers):
    oddslist = []
    for bookmaker in bookmakers:
        bookmakername = bookmaker["name"]
        bets = bookmaker["bets"]
        for bet in bets:
            if bet["name"] == predictedbet["bettype"]:
                bettypelist =  bet["values"]
                for item in bettypelist:
                    if item["value"] == predictedbet["value"]:
                        odds = item["odd"]
                        bookmakerodds =  {"bookmaker": bookmakername, "value": odds}
                        oddslist.append(bookmakerodds)
                        break

    return  oddslist