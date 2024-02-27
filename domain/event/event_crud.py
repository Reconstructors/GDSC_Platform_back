from datetime import datetime
from sqlalchemy.orm import Session

from models import Event  # 실제 모델 경로에 맞춰 수정
from domain.event.event_schema import EventCreate, EventUpdate  # 실제 스키마 경로에 맞춰 수정

def get_event_list(db: Session, skip: int = 0, limit: int = 8, status: str|None = None):
    query = db.query(Event)
    if status:
        query = query.filter(Event.status == status)
    total = query.count()
    event_list = query.order_by(Event.start.desc()).offset(skip).limit(limit).all()
    return total, event_list  # 전체 건수와 페이징 적용된 이벤트 목록 반환

def get_event(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    return event

def create_event(db: Session, event_create: EventCreate):
    db_event = Event(
        title=event_create.title,
        start=event_create.start,
        end=event_create.end,
        cohort=event_create.cohort,
        status=event_create.status,
        photo_id=event_create.photo_id,
        location=event_create.location
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: EventUpdate):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        update_data = event_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
        return db_event
    return None  # 이벤트가 존재하지 않는 경우

def delete_event(db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False  # 이벤트가 존재하지 않는 경우
