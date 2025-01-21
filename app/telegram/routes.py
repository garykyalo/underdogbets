from fastapi import APIRouter, Request
from ..config import settings

router = APIRouter()
@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print(data, "payload")
    chat_id = data['message']['chat']['id']
    response = send_message(chat_id)
    print(response, "response")
    return data

import requests

def send_message(chat_id):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": "thank you"
    }
    response = requests.get(url, params=params)
    return response.json()