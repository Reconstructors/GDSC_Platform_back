from pydantic import BaseModel, Field, constr, field_validator
from typing import List, Tuple, Optional
from datetime import datetime
from enum import Enum

# 가능한 상태 값
class ProjectStatus(str, Enum):
    PLANNING = "Planning"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    CANCELED = "Canceled"

class Project(BaseModel):
    id: int
    title: str
    start: datetime
    end: datetime | None = None
    description: str
    contact_info: List[str] | None = []
    status: str | None = None # 수정 필요
    photo_ids: List[str] | None = []
    create_date: datetime
    modify_date: datetime | None = None
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title: str
    start: datetime
    end: datetime | None = None
    description: str
    contact_info: List[str] | None = []
    status: str | None = None # 수정 필요
    photo_ids: List[str] | None = []
    create_date: datetime

    @field_validator('title', 'description')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class ProjectUpdate(BaseModel):
    title: str
    start: datetime
    end: datetime | None = None
    description: str
    contact_info: List[str] | None = []
    status: str | None = None # 수정 필요
    photo_ids: List[str] | None = []
    modify_date: datetime

class ProjectList(BaseModel):
    total: int=0
    project_list: list[Project] = []

class ProjectDelete(BaseModel):
    project_id: int

from pydantic import BaseModel, Field, validator

class UserProjectMatch(BaseModel):
    id: Optional[int] = None
    user_id: int
    project_id: int
    is_approved: bool
    is_leader: bool
    match_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

class UserProjectMatchCreate(BaseModel):
    user_id: int
    project_id: int
    is_approved: bool = False  # 기본적으로 승인되지 않음
    is_leader: bool = False    # 기본적으로 리더가 아님

    @validator('user_id', 'project_id')
    def id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('ID는 양수이어야 합니다.')
        return v

class UserProjectMatchUpdate(BaseModel):
    is_approved: Optional[bool] = None
    is_leader: Optional[bool] = None

class UserProjectMatchDelete(BaseModel):
    match_id: int
