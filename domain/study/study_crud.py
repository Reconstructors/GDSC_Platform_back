
from datetime import datetime
from sqlalchemy.orm import Session

from domain.study.study_schema import StudyCreate, StudyUpdate
from models import Study, User
from sqlalchemy.orm import Session

from domain.study import study_schema

def get_study_list(db: Session, skip: int = 0, limit: int = 10):
    _study_list = db.query(Study).order_by(Study.create_date.desc())

    study_list = _study_list.offset(skip).limit(limit).all()
    return study_list

def get_study(db: Session, study_id: int) -> study_schema.StudyInDB:
    study = db.query(Study).get(study_id)
    return study

def create_study(db: Session, study_create: StudyCreate, user_id: int):
    db_study = Study(
        title=study_create.title,
        start=study_create.start,
        end=study_create.end,
        description=study_create.description,
        contact_info=study_create.contact_info,
        status=study_create.status,
        photo_ids={},
        create_date= datetime.now(),
        modify_date= datetime.now(),

        owner_id= user_id
    )
    db.add(db_study)
    db.commit()

# TODO: 이렇게 수정하면 안됨
def update_study(db: Session, db_study: Study,
                    study_update: StudyUpdate):
    
    update_data = study_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_study, key, value)

    db_study.modify_date = datetime.now()

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