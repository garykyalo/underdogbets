import requests
from ..config import settings
import os




async def send_message(text):
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    params = {        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
        }
    response = requests.get(telegram_url, params=params)
    return response.status_code




async def send_image(text):
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendPhoto"
    image_url = f"{settings.BASIC_URL}/static/pic.png"
  
    image_path = os.path.abspath("app/static/pic.png")
  

    files = {
        "photo": open(image_path, "rb")  
    }
    
    # Include the photo URL in the 'data' dictionary, not 'params'
    data = {
    "chat_id": chat_id,
    "photo": "https://drive.google.com/file/d/1bfW97sPHSQXgH2KNKDfPQ9o3O1JvVvz_/view",
    "caption": text,
    "parse_mode": "HTML",
}

    # Sending the request with the correct parameters
    response = requests.post(telegram_url, data=data)  
    return response.status_code, response.text


