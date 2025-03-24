from sqlalchemy import Column, Integer, String, Date, Time, PickleType
from app.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    recurring_days_of_week = Column(PickleType, nullable=True)
