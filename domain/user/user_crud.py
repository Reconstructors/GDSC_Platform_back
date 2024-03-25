from passlib.context import CryptContext # 암호 해싱(비밀번호 암호화 및 검증)
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
    db.refresh(db_user) # db_user 인스턴스의 최신 상태를 로드. user의 id가 추가됨.
    return db_user


# user id로 사용자 정보 가져오기
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# user id로 사용자 정보 가져오기
def get_user_by_id(db: Session, user_id:int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

# user id list로 유저 정보 리스트 가져오기
def get_users_by_id_list(db: Session, user_id_list:list[int]):
    return (
        db.query(User)
        .filter(User.id.in_(user_id_list))
        .all()
    )

# 조건에 맞는 유저 정보 목록 가져오기
# skip, limit에 None을 전달하면, 해당 조건을 적용하지 않겠다는 의미
def get_user_list(
    db: Session,
    skip: int = None,
    limit: int = None,
    cohort: int = None,
    position: str = None,
):
    query = db.query(User)
    
    # 기수 필터 적용
    if cohort is not None:
        query = query.filter(User.cohort == cohort)
    
    # 직급 필터 적용
    if position is not None:
        query = query.filter(User.position == position)
    
    # Pagination 적용
    users = query.offset(skip).limit(limit).all()
    return users



def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = (
        db.query(User).filter(User.id == user_id).first()
    )
    update_data = user_update.model_dump(exclude_unset=True)
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