# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from .services.telegram import send_message,send_image
from .services.messages import Daily_tip, populate_message_data
from .services.fetchdata import get_fixtures, get_predictions
from .services.staticfetch import get_teams
from .database import get_db



def sync_fetch_teams():
    db = next(get_db())
    asyncio.run(get_teams(db))

def sync_fetch_fixtures_and_predictions():
    db = next(get_db())
    asyncio.run(get_fixtures(db))
    asyncio.run(get_predictions(db))

# Wrap the async call to ensure an event loop is created in the thread
def sync_send_daily_tip():
    db = next(get_db())
    text, fixtureId, imageurl = asyncio.run(send_daily_tip()) 
    asyncio.run(send_message(db, text, fixtureId)) 

def sync_send_daily_tip_image():
    db = next(get_db())
    result = asyncio.run(send_daily_tip())
    if result is None:
        print("No daily tip to send.")
        return
    text, fixtureId, imageurl = result
    asyncio.run(send_image( db, text, imageurl, fixtureId)) 


async def send_daily_tip():
    db = next(get_db())
    match = await populate_message_data(db)
    if not match:
        return None
    fixtureId = match["fixture_id"]
    imageurl = match["leaguelogo"]
    text = Daily_tip(match)
    return text, fixtureId, imageurl


scheduler = BackgroundScheduler()


# Add the job to the scheduler
scheduler.add_job(
    sync_send_daily_tip_image,
    IntervalTrigger(seconds=1800),
    id="daily_tip_job",
    name="Send Daily Tip",
    replace_existing=True
)

scheduler.add_job(
    sync_fetch_fixtures_and_predictions,
      IntervalTrigger(seconds=7200),
    id="update_predictions",
    name="Update the fixtures and predictions",
    replace_existing=True
)

scheduler.add_job(
    sync_fetch_teams,
      IntervalTrigger(seconds=86400),
    id="update_predictions",
    name="Update the fixtures and predictions",
    replace_existing=True
)

def start_scheduler():
    """Start the scheduler."""
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    """Gracefully stop the scheduler."""
    scheduler.shutdown()
