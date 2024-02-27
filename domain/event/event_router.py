from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from database import get_db
from domain.event import event_schema, event_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(prefix= "/api/event", tags=["Event"])

@router.get("/list", response_model=event_schema.EventList)
def event_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _event_list = event_crud.get_event_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'event_list': _event_list
    }

@router.get("/detail/{event_id}", response_model=event_schema.Event)
def event_detail(event_id: int, db: Session = Depends(get_db)):
    event = event_crud.get_event(db, event_id=event_id)
    return event

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def event_create(_event_create: event_schema.EventCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    event_crud.create_event(db=db, event_create=_event_create,
                                  user=current_user)
    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def event_update(_event_update: event_schema.EventUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_event = event_crud.get_event(db, event_id=_event_update.event_id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_event.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    event_crud.update_event(db=db, db_event=db_event,
                                  event_update=_event_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def event_delete(_event_delete: event_schema.EventDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_event = event_crud.get_event(db, event_id=_event_delete.event_id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_event.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    event_crud.delete_event(db=db, db_event=db_event)