from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router
from .schedular import start_scheduler


def create_app() -> FastAPI:
    app = FastAPI()
    #routes 
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(router)
    start_scheduler()
    return app
