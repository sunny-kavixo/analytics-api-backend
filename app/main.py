from fastapi import Depends, FastAPI, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import Event
from .schemas import EventCreate, EventOut, Summary

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/events", response_model=EventOut, status_code=201)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = Event(**payload.model_dump())
    db.add(event); db.commit(); db.refresh(event)
    return event

@app.get("/events", response_model=list[EventOut])
def list_events(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    return db.scalars(select(Event).order_by(Event.created_at.desc()).limit(limit)).all()

@app.get("/analytics/summary", response_model=Summary)
def analytics_summary(db: Session = Depends(get_db)):
    total, users, total_value, avg_value = db.execute(
        select(func.count(Event.id), func.count(func.distinct(Event.user_id)),
               func.coalesce(func.sum(Event.value), 0.0), func.coalesce(func.avg(Event.value), 0.0))
    ).one()
    return Summary(total_events=total, unique_users=users, total_value=total_value, average_value=avg_value)
