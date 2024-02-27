
from datetime import datetime
from sqlalchemy.orm import Session

from domain.study.study_schema import StudyCreate, StudyUpdate
from models import Study, User
from sqlalchemy.orm import Session

def get_study_list(db: Session, skip: int = 0, limit: int = 10):
    _study_list = db.query(Study).order_by(Study.create_date.desc())
    total = _study_list.count()
    study_list = _study_list.offset(skip).limit(limit).all()
    return total, study_list

def get_study(db: Session, study_id: int):
    study = db.query(Study).get(study_id)
    return study

def create_study(db: Session, study_create: StudyCreate):
    db_study = Study(
        title=study_create.title,
        start=study_create.start,
        end=study_create.end,
        description=study_create.description,
        contact_info=study_create.contact_info,
        status=study_create.status,
        photo_ids=study_create.photo_ids,
    )
    db.add(db_study)
    db.commit()

def update_study(db: Session, db_study: Study,
                    study_update: StudyUpdate):
    db_study.title = study_update.title
    db_study.start = study_update.start
    db_study.modify_date = datetime.now()
    db_study.end = study_update.end
    db_study.description = study_update.description
    db_study.contact_info = study_update.contact_info
    db_study.status = study_update.status
    db_study.photo_ids = study_update.photo_ids
    db.add(db_study)
    db.commit()

def delete_study(db: Session, db_study: Study):
    db.delete(db_study)
    db.commit()

# def create_study_match(db: Session, study_match: studies_schemas.StudyMatchCreate):
#     db_study_match = studies_models.StudyMatch(
#         user_id = study_match.user_id,
#         study_id = study_match.study_id,
#         is_approved = study_match.is_approved,
#         is_leader = study_match.is_leader
#     )
#     db.add(db_study_match)
#     db.commit()
#     db.refresh(db_study_match)
#     return db_study_match

# def get_study_match(db: Session, match_id: int):
#     return db.query(studies_models.StudyMatch).filter(studies_models.StudyMatch.id == match_id).first()

# def get_study_matches(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(studies_models.StudyMatch).offset(skip).limit(limit).all()