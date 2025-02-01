from openai import OpenAI
from .config import settings
import re, json
from .database import Fixtures, Prediction, Odds
from sqlalchemy.orm import Session

client = OpenAI(api_key=settings.OPENAI_KEY)

async def get_openai_response(prompt: str) -> str:
    response = client.chat.completions.create(
    messages=[
                {
                    "role": "user",
                "content": prompt,
                }
            ],
            model="gpt-4o",
        )
        # Extract the generated response text
    generated_text = response.choices[0].message.content.strip()
    print(response)
    return generated_text

async def generate_odds(db:Session):
    prediction_query = db.query(Prediction).filter(Prediction.fixture_id ==1293561).first()
    odds_query = db.query(Odds).filter(Odds.fixture_id ==1293561).first()
    prediction = {column.name: getattr(prediction_query, column.name) for column in Prediction.__table__.columns}
    odds = {column.name: getattr(odds_query, column.name) for column in Odds.__table__.columns}
    prompt = f"""
Based on the prediction: "{prediction}",
iterate over the following odds and identify the single bookmaker with the highest combined odds for both the Double Chance and Under 3.5 Goals.

{odds}

Return the result as a JSON object in this format:

{{
  "bet_recommendation": {{
    "bet": "Combo Double Chance (Deportivo W or Draw) + Under 3.5 Goals",
    "best_odds": {{
      "bookmaker": "<bookmaker_name>",
      "double_chance_odds": <double_chance_odds>,
      "under_3_5_odds": <under_3_5_odds>
    }}
  }}
}}
"""

    response_text = await get_openai_response(prompt)

# Regex pattern to match the JSON part
    pattern = r'```json\n({.*?})\n```'

# Search for the JSON block
    match = re.search(pattern, response_text, re.DOTALL)

    if match:
        json_data = json.loads(match.group(1))  # Parse the matched JSON
        print(json_data)
    else:
        json_data = response_text  # Return the full text if no JSON found
        print("No JSON found.")
    return json_data

