from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List

class ParticipantBase(BaseModel):
    name: str
    email: EmailStr

class ParticipantCreate(ParticipantBase):
    event_id: int

class Participant(ParticipantBase):
    id: int
    event_id: int
    
    class Config:
        from_attributes = True

class ParticipantPublic(BaseModel):
    name: str
    
    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    date: date
    location: str
    quota: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        from_attributes = True