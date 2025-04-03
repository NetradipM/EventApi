from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

Base = declarative_base()

class EventStatus(enum.Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"

class Event(Base):
    __tablename__ = 'events'
    
    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    max_attendees = Column(Integer)
    status = Column(Enum(EventStatus), default=EventStatus.scheduled)

class Attendee(Base):
    __tablename__ = 'attendees'
    
    attendee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    check_in_status = Column(Boolean, default=False)
