import os
from typing import List
from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context
from domain.auth.dependencies import get_current_user_id


from dotenv import load_dotenv
load_dotenv()

# 환경 변수 load
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


router = APIRouter(prefix="/api/user", tags=["Account"])

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

# 유저 생성하기 (회원가입)
@router.post("/create", response_model=user_schema.UserOut)
def create_user(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    유저 생성하기 (회원가입)

    이 API는 새로운 사용자를 생성합니다.
    이미 존재하는 사용자의 username이 입력되면 409 에러를 반환합니다.
    """
    user = user_crud.get_user_by_username(db, username=user_create.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")
    return user_crud.create_user(db=db, user_create=user_create)

# username 중복확인
@router.post("/duplicate")
def check_duplicate(username: str, db: Session = Depends(get_db)):
    """
    username 중복확인

    이 API는 username 중복확인을 합니다. 회원가입을 요청하기 전에 username 중복확인을 꼭 하시기 바랍니다.
    이미 존재하는 사용자의 username이 입력되면 409 에러를 반환합니다.
    """
    user = user_crud.get_user_by_username(db, username=username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")

# 유저 로그인
@router.post("/login", response_model= user_schema.Token)
def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    """
    유저 로그인

    이 API는 이미 존재하는 계정에 대한 username과 password를 입력하면 JWT 토큰을 반환합니다.\n
    존재하지 않는 유저이면 404 에러를 반환합니다.\n
    올바르지 않은 username 또는 password를 입력하면 401 에러를 반환합니다.
    """
    user = user_crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # JWT access token 생성
    expires=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user.id),
        "iat": datetime.now(),
        "exp": expires
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(key="access_token", value=access_token, expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), httponly=True)

    return user_schema.Token(access_token=access_token, token_type="bearer")


# 조건에 맞는 모든 유저 목록 불러오기
@router.get("/user_list", response_model=list[user_schema.UserOut])
def read_user_list(
        skip: int | None = None, 
        limit: int | None = None, 
        cohort: int | None = None, 
        position: str| None=None, 
        db: Session = Depends(get_db)
    ):
    """
    조건에 맞는 유저 목록 불러오기
    
    이 API는 조건에 맞는 모든 유저의 정보를 반환합니다.\n
    아무런 조건을 입력하지 않으면, 모든 유저의 정보를 반환합니다.\n
    """
    return user_crud.get_user_list(db=db, skip=skip, limit=limit, cohort=cohort, position=position)



# id로 한 유저의 정보 불러오기
@router.get("/{user_id}", response_model=user_schema.UserOut)
async def read_user(
        user_id: int,
        db: Session = Depends(get_db)):
    """
    id로 한 유저의 정보 불러오기
    
    이 API는 user_id에 맞는 유저의 정보를 반환합니다.\n
    user_id에 해당하는 유저가 없으면 404 에러를 반환합니다.\n
    """

    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# id로 유저 정보 수정하기
@router.patch("/{user_id}", response_model=user_schema.User)
async def update_user(
        user_id: int,
        user_update: user_schema.UserUpdate,
        token_user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    """
    내 정보 수정하기
    
    이 API는 내 계정 정보를 수정합니다.\n
    수정 권한이 없는 계정에 대한 요청 시 401 에러를 반환합니다.\n
    user_id에 해당하는 유저가 없으면 404 에러를 반환합니다.\n
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"},
    )

    if user_id != token_user_id:
        raise credentials_exception

    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_crud.update_user(db=db, user_id=user_id, user_update=user_update)
    return db_user

# 회원탈퇴
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int, 
        token_user_id: int = Depends(get_current_user_id),
        db: Session=Depends(get_db)
    ):
    """
    회원탈퇴하기
    
    이 API는 계정에 대한 회원탈퇴를 합니다.\n
    탈퇴 권한이 없는 계정에 대한 요청 시 401 에러를 반환합니다.\n
    user_id에 해당하는 유저가 없으면 404 에러를 반환합니다.\n
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"},
    )

    if user_id != token_user_id:
        raise credentials_exception

    deleted_user = user_crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return None




