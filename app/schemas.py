from pydantic import BaseModel
from datetime import date, time
from typing import Optional, Set

class EventBase(BaseModel):
    name: str
    start_date: date
    start_time: time
    duration_minutes: int
    recurring_days_of_week: Optional[Set[int]] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    start_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    recurring_days_of_week: Optional[Set[int]] = None

class EventInDB(EventBase):
    id: int
    class Config:
        orm_mode = True
