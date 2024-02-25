from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import account_crud
from ..schemas import account_schemas
from ..models import account_models
from ..dependencies import get_db

router = APIRouter(tags=["Account"])

# 유저 목록 불러오기
@router.get("/api/users", response_model=List[account_schemas.User], description="유저 목록 불러오기")
def read_users(skip: int=0, limit: int=8, cohort: int | None = None, position:str|None=None, db: Session = Depends(get_db)):
    return account_crud.get_users(db=db, skip=skip, limit=limit, cohort=cohort, position=position)

# id로 유저 불러오기
@router.get("/api/users/{user_id}", response_model=account_schemas.User, description="id로 유저 불러오기")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = account_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 유저 생성하기 (회원가입)
@router.post("/api/account/signup/")
def create_user(user: account_schemas.UserCreate, db: Session = Depends(get_db), description="유저 생성하기 (회원가입)"):
    db_user = account_crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return account_crud.create_user(db=db, user=user)

# id로 유저 정보 수정하기
@router.patch("/api/account/{user_id}", response_model=account_schemas.User)
def update_user(user_id: int, user_update: account_schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(account_models.User).filter(account_models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    # 여기에 정보 수정 코드 작성
    db.commit()
    db.refresh(db_user)
    return db_user

# id로 유저 정보 삭제하기
@router.delete("/api/account/{user_id}",response_model=account_schemas.User)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    deleted_user = account_crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return deleted_user

@router.post("/api/account/login/")
def login(token_data: account_schemas.JWTTokenData, db: Session = Depends(get_db)):
    user_info = account_crud.authenticate_user(token_data.token)
    print(token_data.token)
    if user_info:
        db_user = account_crud.get_user_by_email(db, email=user_info['email'])
        print(db_user)
        print("help")
        return {"message": "Token received and verified", "user_info": user_info}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")