from sqlalchemy.orm import Session

from ..models import event_models
from ..schemas import event_schemas

def get_event(db: Session, event_id: int):
    return db.query(event_models.Event).filter(event_models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 8, status: str|None = None):
    if status==None:
        return db.query(event_models.Event).offset(skip).limit(limit).all()
    else:
        return db.query(event_models.Event).filter(event_models.Event.status == status).offset(skip).limit(limit).all()

def create_event(db: Session, event: event_schemas.EventCreate):
    db_event = event_models.Event(
        title=event.title,
        start=event.start,
        end=event.end,
        cohort=event.cohort,
        status=event.status,
        photo_id=event.photo_id,
        location = event.location
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: event_schemas.EventUpdate):
    db_event = db.query(event_models.Event).filter(event_models.Event.id == event_id).first()
    update_data = event_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db:Session, event_id: int):
    db_event = db.query(event_models.Event).filter(event_models.Event.id == event_id).first()
    if not db_event:
        return None
    db.delete(db_event)
    db.commit()
    return db_event