from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import event_crud
from ..schemas import event_schemas
from ..models import event_models
from ..dependencies import get_db

router = APIRouter(tags=["Event"])

# 스터디 목록 불러오기
@router.get("/api/events", response_model=List[event_schemas.Event], description="이벤트 목록 불러오기")
def read_event(skip: int=0, limit: int=8, status: str|None = None, db: Session = Depends(get_db)):
    return event_crud.get_events(db=db, skip=skip, limit=limit, status=status)

# id로 스터디 불러오기
@router.get("/api/event/{event_id}", response_model=event_schemas.Event, description="ID로 이벤트 불러오기")
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = event_crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="event not found")
    return db_event

# 이벤트 생성하기
@router.post("/api/event/", response_model=event_schemas.Event, description="이벤트 생성하기")
def create_event(event: event_schemas.EventCreate, db: Session = Depends(get_db)):
    return event_crud.create_event(db=db, event=event)

# id로 이벤트 수정하기
@router.patch("/api/event/{event_id}", response_model=event_schemas.Event)
def update_event(event_id: int, event_update: event_schemas.EventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(event_models.Event).filter(event_models.event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="event not found")
    if event_update.title is not None:
        db_event.title = event_update.title
    if event_update.start is not None:
        db_event.start = event_update.start
    db.commit()
    db.refresh(db_event)
    return db_event

# id로 이벤트 삭제하기
@router.delete("/api/event/{event_id}",response_model=event_schemas.Event)
def delete_event(event_id: int, db: Session=Depends(get_db)):
    deleted_event = event_crud.delete_event(db=db, event_id=event_id)
    if deleted_event is None:
        raise HTTPException(status_code=404, detail="event not found")
    return deleted_event