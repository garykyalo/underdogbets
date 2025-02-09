from fastapi import FastAPI
from . import routes
from . import endpoints
from .schedular import start_scheduler


def create_app() -> FastAPI:
    app = FastAPI()
    #routes 
    app.include_router(routes.router)
    app.include_router(endpoints.router)
    #start_scheduler()
    return app
