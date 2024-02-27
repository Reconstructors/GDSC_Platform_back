from pydantic import BaseModel, Field, constr, EmailStr, field_validator
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum
from pydantic_core.core_schema import FieldValidationInfo

class User(BaseModel):
    username: str
    email: EmailStr
    cohort: int # 기수
    position: str # 직급
    bio: str | None = None
    description: str | None = None
    links: List[str] | None = None  # JSON 형태의 문자열로 저장
    interests: List[str] | None = []  # 관심분야, 리스트 타입
    project_interest: Optional[bool] = None

class UserCreate(User):
    password1: str
    password2: str

    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class UserUpdate(User):
    pass

# class GoogleTokenData(BaseModel):
#     token: str = Field()

# class JWTTokenData(BaseModel):
#     email: str | None=None
