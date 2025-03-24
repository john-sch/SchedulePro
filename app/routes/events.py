from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import models, schemas
from app.services import events_overlap

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.EventInDB, status_code=status.HTTP_201_CREATED)
def create_event(event_in: schemas.EventCreate, db: Session = Depends(get_db)):
    all_events = db.query(models.Event).all()
    for e in all_events:
        if events_overlap(event_in.start_date, event_in.start_time, event_in.duration_minutes,
                          event_in.recurring_days_of_week, e.start_date, e.start_time, e.duration_minutes, e.recurring_days_of_week):
            raise HTTPException(400, "Event conflicts with an existing event.")
    new_event = models.Event(**event_in.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/", response_model=List[schemas.EventInDB])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@router.get("/{event_id}", response_model=schemas.EventInDB)
def get_event(event_id: int, db: Session = Depends(get_db)):
    evt = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not evt:
        raise HTTPException(404, "Event not found.")
    return evt

@router.put("/{event_id}", response_model=schemas.EventInDB)
def update_event(event_id: int, updates: schemas.EventUpdate, db: Session = Depends(get_db)):
    evt = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not evt:
        raise HTTPException(404, "Event not found.")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(evt, field, value)
    all_events = db.query(models.Event).all()
    for e in all_events:
        if e.id == evt.id:
            continue
        if events_overlap(evt.start_date, evt.start_time, evt.duration_minutes,
                          evt.recurring_days_of_week, e.start_date, e.start_time, e.duration_minutes, e.recurring_days_of_week):
            raise HTTPException(400, "Updated event conflicts with an existing event.")
    db.commit()
    db.refresh(evt)
    return evt

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    evt = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not evt:
        raise HTTPException(404, "Event not found.")
    db.delete(evt)
    db.commit()
    return {"detail": "Event deleted."}
