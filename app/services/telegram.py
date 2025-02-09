import requests,json
from ..config import settings
from sqlalchemy.orm import Session
from ..database import Prediction


async def send_message(db: Session, text, fixtureid, bookmaker, bookmakerwebsite):
    print(bookmakerwebsite, "hii hapa")
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [
                {"text":f"bet on {bookmaker}", "url": f"{bookmakerwebsite}"}
            ]
        ]
    }
    params = {"chat_id": chat_id,                
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard)
        }
    response = requests.get(telegram_url, params=params)
    if response.status_code == 200:
        prediction =  db.query(Prediction).filter(Prediction.fixture_id == fixtureid).first()
        prediction.message_send = True
        db.commit()
    return response.status_code, response.text


async def send_image(db: Session, text, imageurl, fixtureid,bookmaker):
    chat_id = -1002226489488
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendPhoto"   
   
    keyboard = {
        "inline_keyboard": [
            [
                {"text":f"bet on {bookmaker}", "url": f"https://example.com/{bookmaker}"}
            ]
        ]
    }
    
    data = {
    "chat_id": chat_id,
    "photo": imageurl,
    "caption": text,
    "parse_mode": "HTML",
     "reply_markup": json.dumps(keyboard)
}
    
    response = requests.post(telegram_url, data=data)
    if response.status_code == 200:
        prediction =  db.query(Prediction).filter(Prediction.fixture_id == fixtureid).first()
        prediction.message_send = True
        db.commit()  
    print("this was called")
    return response.status_code, response.text


