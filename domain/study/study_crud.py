
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

# 쓸 일 없을 듯
# def get_study_match(db: Session, match_id: int):
#     return db.query(UserStudyMatch).get(UserStudyMatch.id == match_id)

# 스터디 id와 user id로 match 정보 불러오기
def get_study_match_by_study_id_user_id(db: Session, study_id: int, user_id: int):
    return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.user_id == user_id).first()

# 스터디 id로 match 목록 불러오기
# 1. 승인된 목록만
# 2. 비승인된 목록만
# 3. 모두
def get_study_matches_by_study_id(db: Session, study_id: int, only_approved: bool, only_unapproved:bool):
    if only_approved:
        return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.is_approved == True).all()
    elif only_unapproved:
        return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.is_approved == False).all()
    else:
        return db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id).all()

# 스터디 id로 승인된 스터디 참가자 id 정보 불러오기
def get_approved_user_ids_by_study_id(db: Session, study_id: int) -> list[int]:
    matches = get_study_matches_by_study_id(db=db, study_id=study_id, only_approved=True, only_unapproved=False)
    user_ids = [match.user_id for match in matches]
    return user_ids

# 스터디 id로 승안 안된 스터디 참가자 id 정보 불러오기
def get_unapproved_user_ids_by_study_id(db: Session, study_id: int) -> list[int]:
    matches = get_study_matches_by_study_id(db=db, study_id=study_id, only_approved=False, only_unapproved=True)
    user_ids = [match.user_id for match in matches]
    return user_ids

def get_study_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserStudyMatch).offset(skip).limit(limit).all()


# user id에 대한 스터디 참가 승인 or 비승인으로 전환
def change_study_match_staus(db: Session, study_id:int, user_id:int, approved:bool):
    db_match = db.query(UserStudyMatch).filter(UserStudyMatch.study_id==study_id, UserStudyMatch.user_id==user_id).first()
    
    if db_match:
        db_match.is_approved = approved
        db.commit()
        db.refresh(db_match)
        return db_match
    else:
        None
    
# 스터디 탈퇴하기
def delete_study_match(db: Session, db_study_match: UserStudyMatch):
    db.delete(db_study_match)
    db.commit()

# study_id에 해당하는 study match 전부 삭제
def delete_study_matches_by_study_id(db: Session, study_id: int):
    db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id).all().delete()
    db.commit()

# user_id에 해당하는 모든 study match 삭제
# 회원탈퇴 시 사용할 수 있을 듯
def delete_study_matches_by_user_id(db: Session, user_id: int):
    db.query(UserStudyMatch).filter(UserStudyMatch.user_id == user_id).all().delete()
    db.commit()

def change_study_leader(db: Session, study_id:int, original_leader_id: int, next_leader_id:int):
    db_match_org = db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.user_id == original_leader_id).first()
    db_match_org.is_leader = False

    db_match_new = db.query(UserStudyMatch).filter(UserStudyMatch.study_id == study_id, UserStudyMatch.user_id == next_leader_id).first()
    db_match_new.is_leader = True

    db.commit()

