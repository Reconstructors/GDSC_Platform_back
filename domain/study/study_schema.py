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
    status: str | None = None
    # photo_ids: Optional[List[str]] = []  # JSON 필드는 리스트 타입으로 표현
    
    class Config:
        orm_mode = True

class Study(StudyBase):
    id: int
    owner_id: int

class StudyInDB(Study):
    create_date: date
    modify_date: date

class StudyCreate(StudyBase):
    pass

class StudyOut(Study):
    pass

class StudyUpdate(BaseModel):
    title: str | None = None
    start: date | None = None
    end: date | None = None
    description: str | None = None
    contact_info: Optional[List[str]] = []  # JSON 필드는 리스트 타입으로 표현
    status: str | None = None




class StudyMatchBase(BaseModel):
    user_id: int
    study_id: int
    is_approved: bool | None = False # 스터디에 포함이 됐는지
    is_leader: bool | None = False # 스터디의 리더인지

class StudyMatchCreate(StudyMatchBase):
    pass

class StudyMatch(StudyMatchBase):
    id: int

    class Config:
        from_attributes = True

class StudyDelete(BaseModel):
    study_id: int