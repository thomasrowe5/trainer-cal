from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import availability

app = FastAPI()

# Allow your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trainercal.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(availability.router, prefix="")

@app.get("/")
def root():
    return {"status": "ok", "message": "TrainerCal backend is live"}

