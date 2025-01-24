from fastapi import APIRouter, Request
from .helpers import send_message
from ..config import settings
import requests

router = APIRouter()
@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    response = await send_message(data)
    return data

@router.get("/set-webhook")
async def set_webhook():
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/setWebhook?url={settings.BASIC_URL}/webhook"
    response = requests.get(url)
    return response.json()


