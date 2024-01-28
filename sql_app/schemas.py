from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

# class ItemBase(BaseModel):
#     title: str
#     description: str | None=None

# class ItemCreate(ItemBase):
#     pass

# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True

# class UserBase(BaseModel):
#     email: str

# class UserCreate(UserBase):
#     password: str

# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []
#     class Config:
#         orm_mode = True
#############################################
class UserBase(BaseModel):
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
    name: str
    email: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    token: str = Field()