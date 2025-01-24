from ..config import settings
import httpx

"""async def extract_from_sportradar():
    
    url = "https://api.sportradar.com/soccer/production/v4/en/seasons"
    params = {
        "api_key": settings.SPORTSRADAR_API_KEY  
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        print(response.status_code, "hii")
        print(response.text)
        return response"""
    
"""import http.client
async def extract_from_sportradar():
    conn = http.client.HTTPSConnection("api.sportradar.com")

    conn.request("GET", f"/beachsoccer/trial/v2/en/competitions/sr%3Acompetition%3A760/info?api_key={settings.SPORTSRADAR_API_KEY}")
    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"), "hapa")
    return data"""

import requests
async def extract_from_sportradar():
    competition_id = "Need to be defined"
    base_url = f"https://api.sportradar.com/beachsoccer/trial/v2/en/competitions/{competition_id}/seasons.json"
   
    basic_url = "https://api.sportradar.com/beachsoccer/trial/v2/en/competitions/sr%3Acompetition%3A1068/seasons.json?"
    url = f"{basic_url}api_key={settings.SPORTSRADAR_API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)


    return response.text