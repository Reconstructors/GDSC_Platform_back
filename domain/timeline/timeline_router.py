from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.timeline import timeline_schema, timeline_crud
from domain.user.user_router import get_current_user_id
from models import User

router = APIRouter(
    prefix="/api/timeline",
    tags=["Timeline"],
)

@router.get("/list", response_model=list[timeline_schema.TimelineOut])
def get_timelines(
        skip: int|None = None, 
        limit: int|None = None, 
        db: Session = Depends(get_db)):
    """
    타임라인 목록 불러오기

    이 API는 타임라인 목록을 불러옵니다.
    """
    _timeline_list = timeline_crud.get_timeline_list(db, skip=skip, limit=limit)

    return _timeline_list

@router.post("/create",response_model= timeline_schema.TimelineOut, status_code=status.HTTP_201_CREATED)
def timeline_create(
        timeline_create: timeline_schema.TimelineCreate,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    """
    타임라인 생성하기

    이 API는 타임라인을 생성합니다.
    """
    _timeline =  timeline_crud.create_timeline(db=db, timeline_create=timeline_create,
                                  user_id=user_id)
    
    return _timeline



@router.patch("/update/{timeline_id}",response_model=timeline_schema.TimelineOut ,status_code=status.HTTP_200_OK)
def timeline_update(
        timeline_id: int,
        timeline_update: timeline_schema.TimelineUpdate,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    """
    타임라인 수정하기

    이 API는 타임라인을 수정합니다.
    수정권한이 없을 경우 401 에러를 반환합니다.
    존재하지 않는 타임라인일 경우 404 에러를 반환합니다.
    """
    db_timeline: timeline_schema.TimelineInDB = timeline_crud.get_timeline(db, timeline_id=timeline_id)

    if db_timeline is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Timeline not found")
    
    
    # TODO: 나중에는 수정권한만 확인하는 식으로 수정
    if user_id != db_timeline.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Update permission denied")
    
    

    _timeline = timeline_crud.update_timeline(db=db, timeline_update=timeline_update, timeline_id=timeline_id)

    return _timeline


@router.delete("/delete/{timeline_id}", status_code=status.HTTP_204_NO_CONTENT)
def timeline_delete(
        timeline_id: int,
        user_id: User = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    """
    타임라인 삭제하게

    이 API는 타임라인을 삭제합니다.
    수정권한이 없을 경우 401 에러를 반환합니다.
    존재하지 않는 타임라인일 경우 404 에러를 반환합니다.
    """
    db_timeline: timeline_schema.TimelineInDB = timeline_crud.get_timeline(db, timeline_id=timeline_id)
    if not db_timeline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Timeline not found")
    # TODO: 나중에는 삭제권한만 확인하는 식으로 수정                            
    if user_id != db_timeline.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Delete permission denied")
    
    timeline_crud.delete_timeline(db=db, db_timeline=db_timeline)