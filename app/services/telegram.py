import requests
from ..config import settings
from sqlalchemy.orm import Session
from ..database import Prediction


async def send_message(db: Session, text, fixtureid):
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    params = {        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
        }
    response = requests.get(telegram_url, params=params)
    if response.status_code == 200:
        prediction =  db.query(Prediction).filter(Prediction.fixture_id == fixtureid).first()
        prediction.message_send = True
        db.commit()
    return response.status_code


async def send_image(db: Session, text, imageurl, fixtureid):
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendPhoto"   
    # Include the photo URL in the 'data' dictionary, not 'params'
    data = {
    "chat_id": chat_id,
    "photo": imageurl,
    "caption": text,
    "parse_mode": "HTML",
}

    # Sending the request with the correct parameters
    response = requests.post(telegram_url, data=data)
    if response.status_code == 200:
        prediction =  db.query(Prediction).filter(Prediction.fixture_id == fixtureid).first()
        prediction.message_send = True
        db.commit()  
    print("this was called")
    return response.status_code, response.text


