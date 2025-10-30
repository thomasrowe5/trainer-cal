from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.availability import router as availability_router
from .routes.checkout import router as checkout_router
from .routes.stripe_webhook import router as stripe_webhook_router
from .routes.bookings import router as bookings_router
from .routes.health import router as health_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://trainercal.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(availability_router)
app.include_router(checkout_router)
app.include_router(stripe_webhook_router)
app.include_router(bookings_router)
app.include_router(health_router)

