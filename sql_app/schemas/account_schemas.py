from pydantic import BaseModel, Field, constr
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum

class UserBase(BaseModel):
    name: str
    email: str
    bio: Optional[str] = None
    description: Optional[str] = None
    links: Optional[str] = None  # JSON 형태의 문자열로 저장
    interests: Optional[List[str]] = []  # 관심분야, 리스트 타입
    participation: Optional[List[Tuple[int, int]]] = []  # 참여 기수 및 직위, 리스트 타입
    project_interest: Optional[bool] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    token: str = Field()
