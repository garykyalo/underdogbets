# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from .services.telegram import send_message, send_image
from .services.messages import Daily_tip, weekly_stat
from .services.oddsapi import select_match



# Wrap the async call to ensure an event loop is created in the thread
def sync_send_daily_tip():
    text = asyncio.run(send_daily_tip()) 
    asyncio.run(send_message(text)) 

async def send_daily_tip():
    match = await select_match()  # Wait for the match asynchronously
    text =  Daily_tip(match)
    print(text, "here")
    return text


scheduler = BackgroundScheduler()


# Add the job to the scheduler
scheduler.add_job(
    sync_send_daily_tip,
    IntervalTrigger(minutes=1),
    id="daily_tip_job",
    name="Send Daily Tip",
    replace_existing=True
)

# Schedule "Weekly Stats" message
def sync_send_weeklystat():
    text = weekly_stat()
    asyncio.run(send_message(text)) 

scheduler.add_job(
    sync_send_weeklystat,
    IntervalTrigger(minutes=30),  # Runs weekly
    id="weekly_stats_job",
    name="Send Weekly Stats",
    replace_existing=True
)



def start_scheduler():
    """Start the scheduler."""
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    """Gracefully stop the scheduler."""
    scheduler.shutdown()
