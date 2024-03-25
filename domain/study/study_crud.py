
from datetime import datetime
from sqlalchemy.orm import Session

from domain.study.study_schema import StudyCreate, StudyUpdate
from models import Study, User, UserStudyMatch
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
        # photo_ids={},
        create_date= datetime.now(),
        modify_date= datetime.now(),
        owner_id= user_id
    )
    db.add(db_study)
    db.commit()
    db.refresh(db_study)

    study_match = UserStudyMatch(
        user_id = user_id,
        study_id = db_study.id,
        is_approved = True,
        is_leader = True
    )

    return db_study

def update_study(db: Session, db_study: Study,
                    study_update: StudyUpdate):
    
    update_data = study_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_study, key, value)

    db_study.modify_date = datetime.now()

    db.add(db_study)
    db.commit()

    db.refresh(db_study)
    return db_study

def delete_study(db: Session, db_study: Study):
    db.delete(db_study)
    db.commit()

def create_study_match(db: Session, study_match_create: study_schema.StudyMatchCreate):
    db_study_match = UserStudyMatch(
        user_id = study_match_create.user_id,
        study_id = study_match_create.study_id,
        is_approved = study_match_create.is_approved,
        is_leader = study_match_create.is_leader
    )
    db.add(db_study_match)
    db.commit()
    db.refresh(db_study_match)
    return db_study_match


def get_study_match(db: Session, match_id: int):
    return db.query(UserStudyMatch).get(UserStudyMatch.id == match_id)

def get_study_match_by_study_id_user_id(db: Session, study_id: int, user_id: int):
    return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.user_id == user_id).first()

# 스터디 id로 스터디 참가자에 대한 모든 match 정보 불러오기(승인여부 관계 x)
def get_study_matches_by_study_id(db: Session, study_id: int):
    return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id).all()

def get_unapproved_study_matches_by_study_id(db: Session, study_id: int, skip:int=0, limit: int=100):
    return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.is_approved==False).offset(skip).limit(limit).all()

# 스터디 id로 승인된 스터디 참가자 id 정보 불러오기
def get_user_ids_by_study_id(db: Session, study_id: int) -> list[int]:
    matches = get_study_matches_by_study_id(db=db, study_id=study_id)
    user_ids = [match.user_id for match in matches if match.is_approved == True]
    return user_ids

def get_unapproved_user_ids_by_study_id(db: Session, study_id: int, skip: int = 0, limit: int = 100) -> list[int]:
    matches = get_unapproved_study_matches_by_study_id(db=db, study_id=study_id)
    user_ids = [match.user_id for match in matches]
    return user_ids

def get_study_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserStudyMatch).offset(skip).limit(limit).all()

def approve_study_match(db: Session, study_id: int, user_id: int):
    db_match = db.query(UserStudyMatch).get(UserStudyMatch.study_id==study_id, UserStudyMatch.user_id==user_id)
    db_match.is_approved = True
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def delete_study_match(db: Session, db_study_match: UserStudyMatch):
    db.delete(db_study_match)
    db.commit()

def delete_study_matches_by_study_id(db: Session, study_id: int):
    db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id).all().delete()
    db.commit()

def delete_study_matches_by_user_id(db: Session, user_id: int):
    db.query(UserStudyMatch).filter(UserStudyMatch.user_id == user_id).all().delete()
    db.commit()

