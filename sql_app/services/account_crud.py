from sqlalchemy.orm import Session

from ..models import account_models
from ..schemas import account_schemas

def get_user(db: Session, user_id: int):
    return db.query(account_models.User).filter(account_models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(account_models.User).filter(account_models.User.email == email).first()

def get_users(db: Session, skip: int =0, limit: int= 100):
    return db.query(account_models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: account_schemas.UserCreate):
    # 새 User 모델 인스턴스 생성
    db_user = account_models.User(
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