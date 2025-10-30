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

# Register all routes
app.include_router(availability.router, prefix="")
app.include_router(checkout.router, prefix="")
app.include_router(stripe_webhook.router, prefix="")
app.include_router(bookings.router, prefix="")
app.include_router(health.router, prefix="")
