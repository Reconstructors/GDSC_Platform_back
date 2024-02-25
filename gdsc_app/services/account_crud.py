from fastapi import HTTPException
from sqlalchemy.orm import Session


from ..models import account_models
from ..schemas import account_schemas
from ..dependencies import get_db


def get_user(db: Session, user_id: int):
    return (
        db.query(account_models.User).filter(account_models.User.id == user_id).first()
    )


def get_user_by_email(db: Session, user_email: str):
    return (
        db.query(account_models.User)
        .filter(account_models.User.email == user_email)
        .first()
    )


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    cohort: int = None,
    position: str = None,
):
    query = db.query(account_models.User)
    # Apply cohort filter if provided
    if cohort is not None:
        query = query.filter(account_models.User.cohort == cohort)
    # Apply position filter if provided
    if position is not None:
        query = query.filter(account_models.User.position == position)
    # Apply pagination and return results
    users = query.offset(skip).limit(limit).all()
    return users


def create_user(db: Session, user: account_schemas.UserCreate):
    # 새 User 모델 인스턴스 생성
    db_user = account_models.User(
        name=user.name,
        email=user.email,
        bio=user.bio,
        cohort=user.cohort,
        position=user.position,
        description=user.description,
        links=user.links,
        interests=user.interests,
        project_interest=user.project_interest,
    )
    # 데이터베이스에 추가 및 커밋
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: account_schemas.UserUpdate):
    db_user = (
        db.query(account_models.User).filter(account_models.User.id == user_id).first()
    )
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = (
        db.query(account_models.User).filter(account_models.User.id == user_id).first()
    )
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


############################################################
