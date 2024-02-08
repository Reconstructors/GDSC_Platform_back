from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import studies_crud
from ..schemas import studies_schemas
from ..dependencies import get_db

router = APIRouter(tags=["Study"])

@router.post("/api/studies/", response_model=studies_schemas.Study)
def create_study(study: studies_schemas.StudyCreate, db: Session = Depends(get_db)):
    return studies_crud.create_study(db=db, study=study)

@router.get("/api/studies/{study_id}", response_model=studies_schemas.Study)
def read_study(study_id: int, db: Session = Depends(get_db)):
    db_study = studies_crud.get_study(db, study_id=study_id)
    if db_study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return db_study

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