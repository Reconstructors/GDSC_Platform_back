from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.orm import Session


from models import User
from domain.user.user_schema import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    # 새 User 모델 인스턴스 생성
    db_user = User(
        username=user_create.username,
        password = pwd_context.hash(user_create.password1),
        email=user_create.email,
        bio=user_create.bio,
        cohort=user_create.cohort,
        position=user_create.position,
        description=user_create.description,
        links=user_create.links,
        interests=user_create.interests,
        project_interest=user_create.project_interest,
    )
    # 데이터베이스에 추가 및 커밋
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(User.email == user_create.email).first()

def get_user(db: Session, username: str):
    return (
        db.query(User).filter(User.username == username).first()
    )

def get_user_by_email(db: Session, user_email: str):
    return (
        db.query(User)
        .filter(User.email == user_email)
        .first()
    )


def get_user_list(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    cohort: int = None,
    position: str = None,
):
    query = db.query(User)
    # Apply cohort filter if provided
    if cohort is not None:
        query = query.filter(User.cohort == cohort)
    # Apply position filter if provided
    if position is not None:
        query = query.filter(User.position == position)
    # Apply pagination and return results
    users = query.offset(skip).limit(limit).all()
    return users





def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = (
        db.query(User).filter(User.id == user_id).first()
    )
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = (
        db.query(User).filter(User.id == user_id).first()
    )
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user