from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database, security
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Campus Event Registration Platform API",
    description="API untuk Proyek UTS Interoperability. (Tugas 6 Bonus)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
db_dependency = Depends(get_db)
admin_dependency = Depends(security.get_api_key)

@app.get("/")
def read_root():
    return {"message": "API Registrasi Event Kampus. Buka /docs untuk dokumentasi."}

@app.get("/events", response_model=List[schemas.Event], tags=["Events"])
def get_all_events(db: Session = db_dependency):
    return db.query(models.Event).all()

@app.post("/events", response_model=schemas.Event, status_code=status.HTTP_201_CREATED, tags=["Admin (Events)"])
def create_event(event: schemas.EventCreate, db: Session = db_dependency, api_key: str = admin_dependency):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.put("/events/{id}", response_model=schemas.Event, tags=["Admin (Events)"])
def update_event(id: int, event: schemas.EventCreate, db: Session = db_dependency, api_key: str = admin_dependency):
    db_event = db.query(models.Event).filter(models.Event.id == id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/events/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Admin (Events)"])
def delete_event(id: int, db: Session = db_dependency, api_key: str = admin_dependency):
    db_event = db.query(models.Event).filter(models.Event.id == id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return

@app.post("/register", response_model=schemas.Participant, status_code=status.HTTP_201_CREATED, tags=["Registration"])
def register_for_event(participant: schemas.ParticipantCreate, db: Session = db_dependency):
    db_event = db.query(models.Event).filter(models.Event.id == participant.event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    participant_count = db.query(models.Participant).filter(models.Participant.event_id == participant.event_id).count()
    if participant_count >= db_event.quota:
        raise HTTPException(status_code=400, detail=f"Event '{db_event.title}' is full")

    db_participant = models.Participant(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

@app.get("/participants", response_model=List[schemas.Participant], tags=["Admin (Participants)"])
def get_all_participants(db: Session = db_dependency, api_key: str = admin_dependency):
    return db.query(models.Participant).all()