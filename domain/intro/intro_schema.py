from pydantic import BaseModel
from datetime import date
import datetime
from typing import Optional


class Timeline(BaseModel):
    id: int
    title: str
    date: date

    class Config:
        from_attributes = True


class TimelineCreate(BaseModel):
    title: str
    date: date
    description: str

class TimelineUpdate(BaseModel):
    timeline_id: int
    title: Optional[str] = None
    description: str | None = None
    date: Optional[datetime.date] = None

class TimeLineList(BaseModel):
    total: int = 0
    timeline_list: list[Timeline] = []

class TimelineDelete(BaseModel):
    timeline_id: int