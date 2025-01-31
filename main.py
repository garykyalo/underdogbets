from app import create_app
from app.database import initialize_database

app = create_app()

if __name__ == "__main__":
    initialize_database()
    import uvicorn
    #uvicorn.run(app)
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
