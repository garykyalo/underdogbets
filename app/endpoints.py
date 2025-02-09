from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .services.fetchdata import get_fixtures, get_predictions
from .services.staticfetch import fetch_data
from .database import get_db

router = APIRouter()

@router.get("/fixtures")
async def teamfixtures(db: Session = Depends(get_db)):
    result = await get_fixtures(db)
    return result

@router.get("/teams")
async def teamfixtures(db: Session = Depends(get_db)):
    endpoint ="teams/statistics"
    params =  {"league": 697,  "season": 2024, "team": 1853}
    result = await fetch_data(endpoint, params)
    return result

@router.get("/odds")
async def odds(db: Session = Depends(get_db)):
    result = await get_predictions(db)
    return result