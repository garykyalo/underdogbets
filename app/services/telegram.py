import requests
from ..config import settings



async def send_message(text):
    chat_id = -1002226489488
    print(text, "hii")
    print(chat_id)
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
        }
    response = requests.get(telegram_url, params=params)
    print(response)
    print(response.text)
    return response.status_code



import requests

async def send_image(text):
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendPhoto"
    image_url = f"{settings.BASIC_URL}/static/pic.png"
    print(image_url)
    
    # Include the photo URL in the 'data' dictionary, not 'params'
    data = {
        "chat_id": chat_id,
        "caption": text, 
        "parse_mode": "HTML",
        "photo": image_url  
    }
    
    response = requests.post(telegram_url, data=data)  
    print(response)
    print(response.text)
    return response.status_code, response.text

