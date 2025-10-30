from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import create_db_and_tables
from .routes import auth_google, availability, bookings, checkout, health, stripe_webhook

app = FastAPI(title="TrainerCal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# include routers
app.include_router(health, prefix="")
app.include_router(auth_google)
app.include_router(availability, prefix="")
app.include_router(checkout, prefix="")
app.include_router(stripe_webhook.router, prefix="")
app.include_router(bookings)
