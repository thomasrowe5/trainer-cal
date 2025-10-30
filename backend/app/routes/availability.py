from datetime import datetime, timedelta

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/availability")
def get_availability(user_id: int = Query(...)):
    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    slots = []
    for i in range(6):
        start = base + timedelta(minutes=30 * i)
        end = start + timedelta(minutes=30)
        slots.append(
            {
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
            }
        )
    return slots
