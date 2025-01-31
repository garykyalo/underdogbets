from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router
from .schedular import start_scheduler


def create_app() -> FastAPI:
    app = FastAPI()
    #routes 
    app.include_router(router)
    start_scheduler()
    return app
