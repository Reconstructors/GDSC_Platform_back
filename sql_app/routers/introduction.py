from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..services import introduction_crud
from ..schemas import introduction_schemas
from ..models import introduction_models
from ..dependencies import get_db

router = APIRouter(tags=["Introduction"])


@router.get("/introduction/timeline", response_model=List[introduction_schemas.Timeline])
def get_timelines(count: int = 7, db: Session = Depends(get_db)):
    return introduction_crud.get_timelines(db=db, count=count)


@router.post("/introduction/timeline", response_model=introduction_schemas.Timeline, status_code=status.HTTP_201_CREATED)
def create_timeline(timeline: introduction_schemas.TimelineCreate, db: Session = Depends(get_db)):
    return introduction_crud.create_timeline(db=db, timeline=timeline)


@router.patch("/introduction/timeline/{timeline_id}", response_model=introduction_schemas.Timeline)
def update_timeline(timeline_id: int, timeline_update: introduction_schemas.TimelineUpdate, db: Session = Depends(get_db)):
    db_timeline = db.query(introduction_models.Timeline).filter(introduction_models.Timeline.id == timeline_id).first()
    if db_timeline is None:
        raise HTTPException(status_code=404, detail="Timeline not found")
    
    if timeline_update.title is not None:
        db_timeline.title = timeline_update.title
    if timeline_update.date is not None:
        db_timeline.date = timeline_update.date

    db.commit()
    db.refresh(db_timeline)
    return db_timeline

@router.delete("/introduction/timeline/{timeline_id}", response_model=introduction_schemas.Timeline)
def delete_timeline(timeline_id: int, db: Session = Depends(get_db)):
    deleted_timeline = introduction_crud.delete_timeline(db=db, timeline_id=timeline_id)
    if deleted_timeline is None:
        raise HTTPException(status_code=404, detail="Timeline not found")
    return deleted_timeline