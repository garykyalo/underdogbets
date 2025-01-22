from fastapi import APIRouter, Request
from .helpers import send_message

router = APIRouter()
@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    response = await send_message(data)
    return data


