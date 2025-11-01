from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import create_db_and_tables
# from .routes.auth_google import router as auth_google_router
from .routes.availability import router as availability_router
from .routes.bookings import router as bookings_router
from .routes.checkout import router as checkout_router
from .routes.health import router as health_router
from .routes.stripe_webhook import router as stripe_webhook_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="TrainerCal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://trainercal.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.on_event("startup")
async def log_routes() -> None:
    import logging

    routes = [route.path for route in app.routes]
    logging.warning(f"Registered routes: {routes}")


app.include_router(availability_router, prefix="/availability")
app.include_router(checkout_router, prefix="/checkout")
app.include_router(stripe_webhook_router, prefix="/webhook")
app.include_router(bookings_router, prefix="/bookings")
app.include_router(health_router)
# app.include_router(auth_google_router)


@app.get("/")
def root():
    return {"status": "ok"}
