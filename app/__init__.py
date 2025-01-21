from fastapi import FastAPI
from . import signalgeneration, whatsapp, telegram

def create_app() -> FastAPI:
    app = FastAPI()
    #routes 
    app.include_router(signalgeneration.routes.router)
    app.include_router(telegram.routes.router)
    return app
