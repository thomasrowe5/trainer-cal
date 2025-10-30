from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()


class Booking(BaseModel):
    id: int
    user_id: int
    start_time: str
    end_time: str
    status: str


BOOKINGS: List[Booking] = []


@router.get("/bookings")
def list_bookings(user_id: int = Query(...)):
    return [b.dict() for b in BOOKINGS if b.user_id == user_id]


class CancelRequest(BaseModel):
    booking_id: int


@router.post("/bookings/cancel")
def cancel_booking(data: CancelRequest):
    for b in BOOKINGS:
        if b.id == data.booking_id:
            b.status = "cancelled"
            return b.dict()
    raise HTTPException(status_code=404, detail="Booking not found")
