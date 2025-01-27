import requests
from ..config import settings 


url = "https://v3.football.api-sports.io/"
baskteballurl = "https://v1.basketball.api-sports.io/"

headers = {
    'x-rapidapi-host': "v1.basketball.api-sports.io",
    'x-rapidapi-key': "XxXxXxXxXxXxXxXxXxXxXxXx"
    }

def fetch_data():
    #endpoint = "odds/bookmakers"    ## gives a list of bookmakers, updated daily
    #endpoint = "/odds?date=2025-01-27"   ## gives odds for prematch updated every 3 hrs
    #endpoint = "/odds/mapping"           ## gives a list of available fixtures id, used in odds endpoint
    #endpoint = "/fixtures?season=2024&league=61"
    endpoint = "leagues" # gives a list of all leagues and league ids, do not change
    
    url = f"{baskteballurl}{endpoint}"
    payload={}
    headers = {
  'x-rapidapi-key': settings.API_FOOTBALL,
  'x-rapidapi-host': 'v1.basketball.api-sports.io'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return  response.json()