from openai import OpenAI
from .config import settings
import re, json

client = OpenAI(api_key=settings.OPENAI_KEY)

async def get_openai_response(prompt: str) -> str:
    response = client.chat.completions.create(
    messages=[
                {
                    "role": "user",
                "content": prompt,
                }
            ],
            model="gpt-4o-mini",
        )
        # Extract the generated response text
    generated_text = response.choices[0].message.content.strip()
    print(response)
    return generated_text

async def generate_odds(bet_advice, oddsresponse):
    print("gpt model called")
    prompt = f"""

iterate over the following odds and identify the single bookmaker with the highest combined odds for {bet_advice}.

{oddsresponse}

Return the result as a JSON object in this format:

{{
  "bet_recommendation": {{
    "bet": "Combo bet1 + bet2",
    "best_odds": {{
      "bookmaker": "<bookmaker_name>",
      "bet1": <bet1 odds>,
      "bet2": <bet2 odds>
    }}
  }}
}}
where bet1 and bet2 are bet names if combo, for instance if combo Double Chance Draw/Away + -2.5, then bet1  is Double Chance Draw/Away and bet2 is uder 2.5. if not combo returnonly a single  bet
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



async def categoriseodds(prediction):
    print("gpt model called")
    prompt = f"""
{prediction}.
the above json file has an advice on the best bet for a match,
restructute the  json file into another json file with the format below, 

{{
    "Bet type": <either Match Winner, Combo, or Double Chance">
    "combo": <true or false>
    "double chance": <Home/draw, Draw/Away, None>
    "Goals Over/Under": <eg "Under 5.5", or None>
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

