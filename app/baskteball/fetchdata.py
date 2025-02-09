from ..config import settings
import requests

async def fetch_data(endpoint, params):
    sport="v1.basketball.api-sports.io"
    url = f"https://{sport}/{endpoint}"
    headers = {
  'x-rapidapi-key': settings.API_FOOTBALL,
  'x-rapidapi-host': sport
    }
    response = requests.request("GET", url, headers=headers,params=params)
    return response.json()