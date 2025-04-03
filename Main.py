from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Event, Attendee, EventStatus
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from datetime import datetime

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    event_id: int

class AttendeeResponse(BaseModel):
    attendee_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    check_in_status: bool

@app.post("/events/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(SessionLocal)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventCreate, db: Session = Depends(SessionLocal)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    return db_event

@app.post("/attendees/", response_model=AttendeeResponse)
def register_attendee(attendee: AttendeeCreate, db: Session = Depends(SessionLocal)):
    event = db.query(Event).filter(Event.event_id == attendee.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.max_attendees <= len(db.query(Attendee).filter(Attendee.event_id == event.event_id).all()):
        raise HTTPException(status_code=400, detail="Max attendees limit reached")
    
    db_attendee = Attendee(**attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

@app.post("/att
