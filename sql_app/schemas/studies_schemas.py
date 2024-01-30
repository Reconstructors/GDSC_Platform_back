from pydantic import BaseModel, Field, constr
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum

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