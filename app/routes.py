from fastapi import APIRouter, Request
from fastapi.responses import  PlainTextResponse
from .config import settings
from .services import send_reply, response_payload, template_payload

router = APIRouter()

@router.api_route("/", methods =["GET","POST"])
async def home ():
    return "welcome"


@router.api_route("/webhook", methods=["GET", "POST"])
async def webhook(request: Request):
    if request.method == "GET":
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")
        if mode == "subscribe" and token == settings.VERIFY_TOKEN:
            return PlainTextResponse(content=challenge)
        else:
            return PlainTextResponse(content="Verification failed", status_code=400) 
    elif request.method == "POST":
        data = await request.json()
        message_data = data['entry'][0]['changes'][0]['value']
        if  "messages" in message_data:
            if 'interactive' in message_data['messages'][0]:
                payload = response_payload(message_data)
                print("interactive")
            else:
                print ("not interactive")
                payload = template_payload(message_data)
            send_reply(payload)   
        return PlainTextResponse(content="POST data received")
    
