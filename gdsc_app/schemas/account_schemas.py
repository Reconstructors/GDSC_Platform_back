from pydantic import BaseModel, Field, constr
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum

class UserBase(BaseModel):
    name: str
    email: str
    cohort: int # 기수
    position: str # 직급
    bio: str | None = None
    description: str | None = None
    links: List[str] | None = None  # JSON 형태의 문자열로 저장
    interests: List[str] | None = []  # 관심분야, 리스트 타입
    project_interest: Optional[bool] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class GoogleTokenData(BaseModel):
    token: str = Field()

class JWTTokenData(BaseModel):
    email: str | None=None
