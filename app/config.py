import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    # whatsap
    WHATSAPP_API_URL: str = os.getenv("WHATSAPP_API_URL")
    PHONE_ID: str = os.getenv("PHONE_ID")
    BUSINESS_ID: str = os.getenv("BUSINESS_ID")
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN")
    ACCESS_TOKEN: str = os.getenv("ACCESS_TOKEN")
  
settings = Settings()