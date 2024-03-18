from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from jose import JWTError, jwt

from database import get_db
from domain.user import user_crud, user_schema

import os
from dotenv import load_dotenv
load_dotenv()

# 환경 변수 load
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# 요청에서 access_token 추출
# 요청의 Authorization 헤더의 value를 추출
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)
async def get_access_token(token: str = Depends(api_key_header)):
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )
    return token.split(" ", 1)[1]  # "Bearer " 부분을 제거하고 토큰만 반환

# JWT 토큰 디코딩 & user_id 반환
async def decode_jwt_token(token: str) -> int:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"},
    )

    try:
        # decode 과정에서 자동으로 exp 필드를 검사함
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    return int(user_id)

# JWT 토큰에서 user_id를 추출하고, db에서 해당 유저의 user_id를 반환
async def get_current_user_id(
            token: str = Depends(get_access_token),
            db: Session = Depends(get_db)) -> user_schema.UserInDB:
    
    user_id = await decode_jwt_token(token)

    user = user_crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id