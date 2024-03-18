from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.study import study_schema, study_crud
from database import get_db
from models import User  # 가정한 사용자 모델 경로

from domain.auth.dependencies import get_current_user_id

router = APIRouter(tags=["Study"], prefix="/api/study")

# 스터디 목록 불러오기
@router.get("/list", response_model=list[study_schema.Study])
def study_list(page: int=0, size: int=10, db: Session = Depends(get_db)):
    _study_list = study_crud.get_study_list(
        db, skip=page*size, limit=size)
    return _study_list
    
# id로 스터디 불러오기
@router.get("/detail/{study_id}", response_model=study_schema.Study)
def study_detail(study_id: int, db: Session = Depends(get_db)):
    study = study_crud.get_study(db, study_id=study_id)
    return study

# 스터디 생성하기
@router.post("/create", status_code=status.HTTP_201_CREATED)
def study_create(_study_create: study_schema.StudyCreate,
                    db: Session = Depends(get_db),
                    user_id: User = Depends(get_current_user_id)):
    
    return study_crud.create_study(db=db, study_create=_study_create,
                                  user_id=user_id)

@router.patch("/update/{study_id}", status_code=status.HTTP_200_OK)
def study_update(
        study_id: int,
        study_update: study_schema.StudyUpdate,
        user_id: User = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    
    db_study = study_crud.get_study(db, study_id=study_id)
    if not db_study:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Study not found")
    if user_id != db_study.owner_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Permission denied")
    
    return study_crud.update_study(db=db, db_study=db_study,
                                  study_update=study_update)

# id로 스터디 삭제하기
@router.delete("/delete/{study_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study(
        study_id: int, 
        user_id: User = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    db_study = study_crud.get_study(db, study_id=study_id)
    if db_study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study not found")
    # 삭제 권한 검사 로직 필요(예시로 추가)
    if user_id != db_study.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    study_crud.delete_study(db=db, study_id=study_id)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def study_delete(_study_delete: study_schema.StudyDelete,
                    db: Session = Depends(get_db),
                    user_id: User = Depends(get_current_user_id)):
    db_study = study_crud.get_study(db, study_id=_study_delete.study_id)
    if not db_study:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if user_id != db_study.owner_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    study_crud.delete_study(db=db, db_study=db_study)