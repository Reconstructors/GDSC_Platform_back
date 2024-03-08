from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db  # 경로는 상황에 따라 조정해주세요.
from domain.intro import intro_crud, intro_schema
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/introduction",
    tags=["Introduction"],
)

@router.get("/list", response_model=intro_schema.TimeLineList)
def get_timelines(db: Session = Depends(get_db), page: int=0, size: int=10):
    total, _timeline_list = intro_crud.get_timeline_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'timeline_list': _timeline_list
    }

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def timeline_create(_timeline_create: intro_schema.TimelineCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    intro_crud.create_timeline(db=db, timeline_create=_timeline_create,
                                  user=current_user)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def timeline_update(_timeline_update: intro_schema.TimelineUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_timeline = intro_crud.get_timeline(db, timeline_id=_timeline_update.timeline_id)
    if not db_timeline:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_timeline.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    intro_crud.update_timeline(db=db, db_timeline=db_timeline,
                                  timeline_update=_timeline_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def timeline_delete(_timeline_delete: intro_schema.TimelineDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_timeline = intro_crud.get_timeline(db, timeline_id=_timeline_delete.timeline_id)
    if not db_timeline:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_timeline.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    intro_crud.delete_timeline(db=db, db_timeline=db_timeline)