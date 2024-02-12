from pydantic import BaseModel, Field, constr
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
    end: Optional[date] = None
    description: Optional[str] = None
    contact_info: Optional[List[str]] = []
    status: Optional[str] = None # 수정 필요
    photo_ids: Optional[List[str]] = []

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True
