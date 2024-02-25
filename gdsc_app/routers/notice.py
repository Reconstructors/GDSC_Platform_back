from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from typing import Annotated

from ..services import notice_crud
from ..schemas import notice_schemas
from ..models import notice_models
from ..dependencies import get_db
# from ..main import oauth2_scheme

router = APIRouter(tags=["Notice"])

# 공지사항 목록 불러오기
@router.get("/api/notice", response_model=List[notice_schemas.Notice], description="공지사항 목록 불러오기")
def read_notice(skip: int=0, limit: int=8, db: Session = Depends(get_db)):
    return notice_crud.get_all_notice(db=db, skip=skip, limit=limit)

# id로 공지사항 불러오기
@router.get("/api/notice/{notice_id}", response_model=notice_schemas.Notice, description="ID로 공지사항 불러오기")
def read_notice(notice_id: int, db: Session = Depends(get_db)):
    db_notice = notice_crud.get_notice(db, notice_id)
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return db_notice

# 공지사항 생성하기
@router.post("/api/notice/", response_model=notice_schemas.Notice, description="공지사항 작성하기")
def create_notice(notice: notice_schemas.NoticeCreate, db: Session = Depends(get_db)):
    return notice_crud.create_notice(db=db, notice=notice)

# id로 공지사항 수정하기
@router.patch("/api/notice/{notice_id}", response_model=notice_schemas.Notice)
def update_notice(notice_id: int, notice_update: notice_schemas.NoticeUpdate, db: Session = Depends(get_db)):
    db_notice = db.query(notice_models.Notice).filter(notice_models.Notice.id == notice_id).first()
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    update_data = notice_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notice, key, value) if hasattr(db_notice, key) else None
    db.commit()
    db.refresh(db_notice)
    return db_notice

# id로 공지사항 삭제하기
@router.delete("/api/notice/{notice_id}", response_model=notice_schemas.Notice)
def delete_notice(notice_id: int, db: Session=Depends(get_db)):
    delete_notice = notice_crud.delete_notice(db=db, notice_id=notice_id)
    if delete_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return delete_notice

# 전체 공지사항 삭제하기
@router.delete("/api/notices/", response_model=bool, status_code=200, description="Delete all notices")
def delete_all(db: Session = Depends(get_db)):
    success = notice_crud.delete_all_notices(db=db)
    if success:
        return True
    else:
        raise HTTPException(status_code=500, detail="Failed to delete notices")
