from pydantic import BaseModel, Field, constr
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum

#############################################
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
        orm_mode = True

class TokenData(BaseModel):
    token: str = Field()

######################################################

# 가능한 상태 값
class ProjectStatus(str, Enum):
    PLANNING = "Planning"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    CANCELED = "Canceled"

class ProjectBase(BaseModel):
    title: str
    start: date
    end: Optional[date] = None
    description: Optional[str] = None
    contact_info: Optional[List[str]] = []
    status: Optional[constr(regex='^(' + '|'.join([status.value for status in ProjectStatus]) + ')$')] = [] # 수정 필요
    photo_ids: Optional[List[str]] = []
    member_ids: List[str]

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True

################################################################
class StudyBase(BaseModel):
    title: str
    start: date
    end: Optional[date] = None
    description: Optional[str] = None
    contact_info: Optional[List[str]] = []  # JSON 필드는 리스트 타입으로 표현
    status: str
    photo_ids: Optional[List[str]] = []  # JSON 필드는 리스트 타입으로 표현

class StudyCreate(StudyBase):
    pass

class Study(StudyBase):
    id: int

    class Config:
        orm_mode = True

class StudyMatchBase(BaseModel):
    user_id: int
    study_id: int
    is_approved: Optional[bool] = False
    is_leader: Optional[bool] = False

class StudyMatchCreate(StudyMatchBase):
    pass

class StudyMatch(StudyMatchBase):
    id: int

    class Config:
        orm_mode = True