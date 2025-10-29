from fastapi import FastAPI
from .db import create_db_and_tables
from .routes import health

app = FastAPI(title="TrainerCal API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# include routers
app.include_router(health.router)

