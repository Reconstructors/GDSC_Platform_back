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
