
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests

from ..dependencies import get_db
from ..models import account_models
from ..schemas import account_schemas
from .account_crud import get_user

# JWT 생성을 위한 비밀키와 알고리즘 설정
SECRET_KEY = "432bc10da312c465fd35c6dcb2af1c68c580b555991284f736a5aaa7655bcf2c"  # 실제 사용시 안전한 키로 설정
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 유효기간 설정 (분 단위)

# Google OAuth2 client ID
CLIENT_ID = "902126570126-k61fod9mop3g2i3hh3r175fq4ba3gufa.apps.googleusercontent.com"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = account_schemas.JWTTokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: Annotated[account_schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def verify_google_oauth2_token(token):
    try:
        # Specify the CLIENT_ID of your app
        userinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return userinfo
    except ValueError:
        # Invalid token
        return None


# Google 토큰을 검증하고 JWT 생성
def authenticate_user(token: str):
    user_info = verify_google_oauth2_token(token)
    if user_info:
        access_token = create_access_token(data={"email": user_info["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")