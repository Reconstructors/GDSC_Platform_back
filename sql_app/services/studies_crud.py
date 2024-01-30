from sqlalchemy.orm import Session

from ..models import studies_models
from ..schemas import studies_schemas


def get_study(db: Session, study_id: int):
    return db.query(studies_models.Study).filter(studies_models.Study.id == study_id).first()

def get_studies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(studies_models.Study).offset(skip).limit(limit).all()

def create_study(db: Session, study: studies_schemas.StudyCreate):
    db_study = studies_models.Study(
        title=study.title,
        start=study.start,
        end=study.end,
        description=study.description,
        contact_info=study.contact_info,
        status=study.status,
        photo_ids=study.photo_ids
    )
    db.add(db_study)
    db.commit()
    db.refresh(db_study)
    return db_study

def create_study_match(db: Session, study_match: studies_schemas.StudyMatchCreate):
    db_study_match = studies_models.StudyMatch(**study_match.dict())
    db.add(db_study_match)
    db.commit()
    db.refresh(db_study_match)
    return db_study_match

def get_study_match(db: Session, match_id: int):
    return db.query(studies_models.StudyMatch).filter(studies_models.StudyMatch.id == match_id).first()

def get_study_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(studies_models.StudyMatch).offset(skip).limit(limit).all()