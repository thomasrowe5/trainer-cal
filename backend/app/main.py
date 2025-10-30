from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import availability, checkout, stripe_webhook, bookings, health

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://trainercal.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (directly — no .router suffix!)
app.include_router(availability, prefix="")
app.include_router(checkout, prefix="")
app.include_router(stripe_webhook, prefix="")
app.include_router(bookings, prefix="")
app.include_router(health, prefix="")

