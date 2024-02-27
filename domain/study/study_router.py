from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.study import study_schema, study_crud
from database import get_db
from domain.user.user_router import get_current_user  # 가정한 사용자 인증 모듈 경로
from models import User  # 가정한 사용자 모델 경로

router = APIRouter(tags=["Study"], prefix="/api/study")

# 스터디 목록 불러오기
@router.get("/list", response_model=study_schema.StudyList)
def study_list(db: Session = Depends(get_db), page: int=0, size: int=10):
    total, _study_list = study_crud.get_study_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'study_list': _study_list
    }
# id로 스터디 불러오기
@router.get("/detail/{study_id}", response_model=study_schema.Study)
def study_detail(study_id: int, db: Session = Depends(get_db)):
    study = study_crud.get_study(db, study_id=study_id)
    return study

# 스터디 생성하기
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def study_create(_study_create: study_schema.StudyCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    study_crud.create_study(db=db, study_create=_study_create,
                                  user=current_user)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def study_update(_study_update: study_schema.StudyUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_study = study_crud.get_study(db, study_id=_study_update.study_id)
    if not db_study:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_study.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    study_crud.update_study(db=db, db_study=db_study,
                                  study_update=_study_update)

# id로 스터디 삭제하기
@router.delete("/delete/{study_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study(study_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_study = studies_crud.get_study(db, study_id=study_id)
    if db_study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study not found")
    # 삭제 권한 검사 로직 필요(예시로 추가)
    if current_user.id != db_study.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    studies_crud.delete_study(db=db, study_id=study_id)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def study_delete(_study_delete: study_schema.StudyDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_study = study_crud.get_study(db, study_id=_study_delete.study_id)
    if not db_study:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_study.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    study_crud.delete_study(db=db, db_study=db_study)