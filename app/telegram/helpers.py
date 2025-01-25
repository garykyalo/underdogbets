import requests, json, random
from ..config import settings  
from ..signalgeneration.helper import get_odds_data
from ..signalgeneration.helpers2 import get_In_Season
from .messages import generate_message


async def send_message(data):
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        send_first_message(chat_id, telegram_url)
    elif 'callback_query' in data:
        chat_id = data['callback_query']['message']['chat']['id']
        result = await get_In_Season(chat_id,telegram_url)
        #sport = data['callback_query']['data']
        #matches = await get_odds_data(sport)
        #betting_tips_message(url, chat_id, matches, sport)
        


def send_first_message(chat_id, url):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Get odds", "callback_data": "basketball"}
            ]
        ]
    }

    # Add the keyboard to the message parameters
    params = {
        "chat_id": chat_id,
        "text": "Welcome to Underdog Tips!, which sport would you like tips on",
        "reply_markup": json.dumps(keyboard)  # Serialize keyboard to JSON string
    }

    response = requests.get(url, params=params)
    return response.json()

def betting_tips_message(url, chat_id, matches, sport):
    random_id = random.choice(list(matches.keys()))
# Fetch the match details
    random_match = matches[random_id]
    text = generate_message(random_match,sport)
    params = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.get(url, params=params)
    return response.json()


