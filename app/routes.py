from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from .config import settings
import requests, os
from .services.oddsapi import get_In_Season


router = APIRouter()


@router.get("/")
def home():
    return "Welcome to underdog tips"

@router.get("/leagues")
async def Leagues():
    result = await get_In_Season()
    return result

@router.get("/image")
def get_image():
    image_path = os.path.join("app", "static", "pic.png")
    return FileResponse(image_path)
### telegram routes 

@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print(data, "hii hapa")
    #response = await send_message(data)
    return data

@router.get("/set-webhook")
async def set_webhook():
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/setWebhook?url={settings.BASIC_URL}/webhook"
    response = requests.get(url)
    return response.json()
