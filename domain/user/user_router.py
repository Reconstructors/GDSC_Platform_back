from typing import List
from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "793d93b60244b303a24d34e50c7944cd2c44f123c6456d89205b94523134ca74"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(prefix="/api/user", tags=["Account"])

# 유저 생성하기 (회원가입)
@router.post("/create")
def create_user(_user_create: user_schema.UserCreate, db: Session = Depends(get_db), description="유저 생성하기 (회원가입)"):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)


@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

# 유저 목록 불러오기
def read_user_list(skip: int=0, limit: int=8, cohort: int | None = None, position:str|None=None, db: Session = Depends(get_db)):
    return user_crud.get_users(db=db, skip=skip, limit=limit, cohort=cohort, position=position)

# 로그인된 유저 정보
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user

# id로 유저 불러오기
@router.get("/api/users/{user_id}", response_model=user_schema.User, description="id로 유저 불러오기")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# id로 유저 정보 수정하기
@router.patch("/api/account/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user_update: user_schema.UserUpdate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    # 여기에 정보 수정 코드 작성
    db.commit()
    db.refresh(user)
    return user

# id로 유저 정보 삭제하기
@router.delete("/api/account/{user_id}",response_model=user_schema.User)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    deleted_user = user_crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return deleted_user
