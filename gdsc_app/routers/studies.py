from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import studies_crud
from ..schemas import studies_schemas
from ..models import studies_models
from ..dependencies import get_db

router = APIRouter(tags=["Study"])

# 스터디 목록 불러오기
@router.get("/api/studies", response_model=List[studies_schemas.Study], description="스터디 목록 불러오기")
def read_study(skip: int=0, limit: int=8, db: Session = Depends(get_db)):
    return studies_crud.get_studies(db=db, skip=skip, limit=limit)

# id로 스터디 불러오기
@router.get("/api/studies/{study_id}", response_model=studies_schemas.Study, description="ID로 스터디 불러오기")
def read_study(study_id: int, db: Session = Depends(get_db)):
    db_study = studies_crud.get_study(db, study_id=study_id)
    if db_study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return db_study

# 스터디 생성하기
@router.post("/api/studies/", response_model=studies_schemas.Study, description="스터디 생성하기")
def create_study(study: studies_schemas.StudyCreate, db: Session = Depends(get_db)):
    return studies_crud.create_study(db=db, study=study)

# id로 프로젝트 수정하기
@router.patch("/api/studies/{study_id}", response_model=studies_schemas.Study)
def update_study(study_id: int, study_update: studies_schemas.StudyUpdate, db: Session = Depends(get_db)):
    db_study = db.query(studies_models.Study).filter(studies_models.Study.id == study_id).first()
    if db_study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    if study_update.title is not None:
        db_study.title = study_update.title
    if study_update.start is not None:
        db_study.start = study_update.start
    db.commit()
    db.refresh(db_study)
    return db_study

# id로 프로젝트 삭제하기
@router.delete("/api/studies/{study_id}",response_model=studies_schemas.Study)
def delete_study(study_id: int, db: Session=Depends(get_db)):
    deleted_study = studies_crud.delete_study(db=db, study_id=study_id)
    if deleted_study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return deleted_study


@router.post("/api/study_matches/", response_model=studies_schemas.StudyMatch)
def create_study_match_endpoint(study_match: studies_schemas.StudyMatchCreate, db: Session = Depends(get_db)):
    return studies_crud.create_study_match(db=db, study_match=study_match)

@router.get("/api/study_matches/{match_id}", response_model=studies_schemas.StudyMatch)
def read_study_match(match_id: int, db: Session = Depends(get_db)):
    db_study_match = studies_crud.get_study_match(db, match_id=match_id)
    if db_study_match is None:
        raise HTTPException(status_code=404, detail="Study match not found")
    return db_study_match

@router.get("/api/study_matches/", response_model=List[studies_schemas.StudyMatch])
def read_study_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    study_matches = studies_crud.get_study_matches(db, skip=skip, limit=limit)
    return study_matches