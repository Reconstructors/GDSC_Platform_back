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

# def get_items(db: Session, skip: int=0, limit: int=100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.model_dump(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item