from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, text, Boolean, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy import event

from .config import settings


engine = create_engine(settings.DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()  
    try:
        yield db 
    finally:
        db.close() 

def initialize_database():
    print("Initializing the database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


class Leagues(Base):
    __tablename__ = 'leagues' 
    id = Column(Integer, primary_key=True)
    league_name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    sport = Column(String(100), nullable=False)
    league_status = Column(String(255), nullable=True) ## in season or off season 
    logo = Column(String(255))
    flag = Column(String(255))
    league_id = Column(Integer)  ## the league Id associated with api data


class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    team_name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    code = Column(String(10))
    logo = Column(String(255))
    image =Column(String(255))

class Fixtures(Base):
    __tablename__ = 'fixtures'
    fixture_id = Column(Integer, primary_key=True)
    time = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.league_id'), nullable=False)
    home_team = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team = Column(Integer, ForeignKey('teams.id'), nullable=False)

class Prediction(Base):
    __tablename__ = 'predictions'
    prediction_id = Column(Integer, primary_key=True)
    fixture_id = Column(Integer, ForeignKey('fixtures.fixture_id'), nullable=False, unique=True)
    predictions_data = Column(Text, nullable=False)  # Storing the whole 'predictions' data as JSON
    advice = Column(String(255), nullable=False)
    is_combo = Column(Boolean, default=False)
    bookmaker = Column(Text, nullable=True)      ## selected bookmaker
    bet_odds = Column(Text, nullable=True)     ### selected bookmaker odd
    message_send = Column(Boolean, default=False)     ## boolean that shows whether the matches bet has been shown
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())  # Automatically updates the time

    # Optional: Define a listener to update the time explicitly
@event.listens_for(Prediction, 'before_update')
def receive_before_update(mapper, connection, target):
        target.time_of_recording = func.now()

class Bookmakers(Base):
    __tablename__ = 'bookmakers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    website = Column(String(255), nullable=False)  
    description = Column(String(255), nullable=False)  

class Bettypes(Base):
    __tablename__ = 'bettypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    