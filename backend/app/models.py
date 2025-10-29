from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str
    stripe_id: Optional[str] = None
    google_refresh_token: Optional[str] = None

class Booking(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    client_name: str
    client_email: str
    start_time: datetime
    end_time: datetime
    status: str = "confirmed"
    payment_id: Optional[str] = None

