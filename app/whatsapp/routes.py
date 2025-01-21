from fastapi import APIRouter, Request
from ..config import settings
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

### send message 
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
@router.get("/send-message")
async def send_message():
    message = client.messages.create(
        body="Hello from Twilio via FastAPI!",
        from_="whatsapp:+14155238886",  
        to="whatsapp:+254716073767"  
    )
    return {"message_sid": message.sid}


### receive mesage 
@router.post("/webhook")
async def receive_message(request: Request):
    form_data = await request.form()
    print(form_data)
    return form_data

