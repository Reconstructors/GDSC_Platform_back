from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db  # 경로는 필요에 따라 수정해주세요.
from domain.notice import notice_schema, notice_crud  # 경로는 필요에 따라 수정해주세요.
from domain.user.user_router import get_current_user  # 경로는 필요에 따라 수정해주세요.
from models import User  # 경로는 필요에 따라 수정해주세요.

router = APIRouter(
    prefix="/api/notice",
    tags=["Notice"]
)

@router.get("/list", response_model=notice_schema.NoticeList)
def notice_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _notice_list = notice_crud.get_notice_list(db, skip=page*size, limit=size)
    return {
        'total': total,
        'notice_list': _notice_list
    }

@router.get("/detail/{notice_id}", response_model=notice_schema.Notice)
def notice_detail(notice_id: int, db: Session = Depends(get_db)):
    notice = notice_crud.get_notice(db, notice_id=notice_id)
    if notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def notice_create(_notice_create: notice_schema.NoticeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notice_crud.create_notice(db=db, notice_create=_notice_create)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def notice_update(_notice_update: notice_schema.NoticeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_notice = notice_crud.get_notice(db, notice_id=_notice_update.notice_id)
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    if current_user.id != db_notice.user_id:  # user_id는 Notice 모델에 맞게 조정해주세요.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    notice_crud.update_notice(db=db, db_notice=db_notice, notice_update=_notice_update)

@router.delete("/delete/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def notice_delete(notice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_notice = notice_crud.get_notice(db, notice_id=notice_id)
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    if current_user.id != db_notice.user_id:  # user_id는 Notice 모델에 맞게 조정해주세요.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    notice_crud.delete_notice(db=db, notice_id=notice_id)
