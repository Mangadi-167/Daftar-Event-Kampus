from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from . import models, schemas, database, security
from .database import engine, get_db, SessionLocal

models.Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal() 
    try:
        first_event = db.query(models.Event).first()
        if first_event is None:
            print("DATABASE KOSONG: Menambahkan data event default PNB...")
            
            event1 = models.Event(
                title="Lomba Web Design TRPL PNB 2025",
                date=date(2025, 11, 15),
                location="Gedung JTI Politeknik Negeri Bali",
                quota=50
            )
            event2 = models.Event(
                title="Kompetisi Capture The Flag (CTF) HMTI",
                date=date(2025, 11, 22),
                location="Aula Direktorat PNB",
                quota=100
            )
            event3 = models.Event(
                title="Guest Lecture: Cybersecurity Trends 2026",
                date=date(2025, 12, 1),
                location="Online via Zoom",
                quota=300
            )
            
            db.add_all([event1, event2, event3])
            db.commit()
            print("Data event default PNB berhasil ditambahkan.")
        else:
            print("Database sudah terisi.")
    finally:
        db.close() 

init_db()

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

db_dependency = Depends(get_db)
admin_dependency = Depends(security.get_api_key)

@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse('index.html')

@app.get("/events", response_model=List[schemas.Event], tags=["Events"])
def get_all_events(db: Session = db_dependency):
    return db.query(models.Event).all()

@app.get("/events/{event_id}/participants", response_model=List[schemas.ParticipantPublic], tags=["Events"])
def get_event_participants(event_id: int, db: Session = db_dependency):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    participants = db.query(models.Participant).filter(models.Participant.event_id == event_id).all()
    return participants

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