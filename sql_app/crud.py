from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int =0, limit: int= 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # 새 User 모델 인스턴스 생성
    db_user = models.User(
        email=user.email,
        name=user.name,
        bio=user.bio,
        description=user.description,
        links=user.links,
        interests=user.interests,
        participation=user.participation,
        project_interest=user.project_interest
    )
    # 데이터베이스에 추가 및 커밋
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

##########################################################################

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        title=project.title,
        start=project.start,
        end=project.end,
        description=project.description,
        contact_info=project.contact_info,
        status=project.status,
        photo_ids=project.photo_ids,
        member_ids=project.member_ids
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

##############################################################################

def get_study(db: Session, study_id: int):
    return db.query(models.Study).filter(models.Study.id == study_id).first()

def get_studies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Study).offset(skip).limit(limit).all()

def create_study(db: Session, study: schemas.StudyCreate):
    db_study = models.Study(
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

def create_study_match(db: Session, study_match: schemas.StudyMatchCreate):
    db_study_match = models.StudyMatch(**study_match.dict())
    db.add(db_study_match)
    db.commit()
    db.refresh(db_study_match)
    return db_study_match

def get_study_match(db: Session, match_id: int):
    return db.query(models.StudyMatch).filter(models.StudyMatch.id == match_id).first()

def get_study_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StudyMatch).offset(skip).limit(limit).all()