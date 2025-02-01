import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    # Twillio
    ACCOUNT_SID: str = os.getenv("ACCOUNT_SID")
    AUTH_TOKEN: str = os.getenv("AUTH_TOKEN")
    
    ##SIgnalgeneration
    ODDS_API_KEY: str = os.getenv("ODDS_API_KEY", "").strip('"')
    SPORTSRADAR_API_KEY: str = os.getenv("SPORTSRADAR_API_KEY").strip('"')
    API_FOOTBALL: str = os.getenv("API_FOOTBALL").strip('"')
    ## Telegram
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN").strip('"')
    BASIC_URL: str = os.getenv("Basicurl").strip('"')
    ## Gemini
    OPENAI_KEY: str = os.getenv("OPENAI_KEY").strip('"')

settings = Settings()