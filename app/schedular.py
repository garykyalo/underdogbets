# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio, httpx
from .config import settings
from .signalgeneration.helpers2 import get_In_Season


async def send_scheduled_message():
    chat_id = -4751420742
    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    result = await get_In_Season(chat_id,telegram_url)
    # Send a simple test message
    #payload = {"chat_id": chat_id, "text": "Hello, World!"}
    #async with httpx.AsyncClient() as client:
     #   response = await client.post(telegram_url, json=payload)
     #   print(f"Message sent: {response.status_code}, {response.json()}")  # Debugging

# Wrap the async call to ensure an event loop is created in the thread
def sync_send_scheduled_message():
    asyncio.run(send_scheduled_message())

scheduler = BackgroundScheduler()
# Add the job to the scheduler
scheduler.add_job(
    sync_send_scheduled_message,  # Use the sync wrapper
    IntervalTrigger(minutes=30),  # Run every 10 seconds for testing
    id="send_message_job",
    name="Send message every 10 seconds",
    replace_existing=True
)



def start_scheduler():
    """Start the scheduler."""
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    """Gracefully stop the scheduler."""
    scheduler.shutdown()
