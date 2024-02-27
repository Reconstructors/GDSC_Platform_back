from pydantic import BaseModel, Field, constr, field_validator
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum

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
    end: date | None = None
    description: str
    contact_info: List[str] | None = []
    status: str | None = None # 수정 필요
    photo_ids: List[str] | None = []

class ProjectCreate(ProjectBase):
    @field_validator('title', 'description')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class ProjectUpdate(ProjectBase):
    project_id: int

class Project(ProjectBase):
    id: int

class ProjectList(BaseModel):
    total: int=0
    project_list: list[Project] = []

class ProjectDelete(BaseModel):
    project_id: int