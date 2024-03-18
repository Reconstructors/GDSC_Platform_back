from pydantic import BaseModel
from datetime import date
import datetime
from typing import Optional


class TimelineBase(BaseModel):
    title: str
    description: str
    date: date

    class Config:
        orm_mode = True

class Timeline(TimelineBase):
    id: int

    class Config:
        orm_mode = True

class TimelineInDB(Timeline):
    user_id: str

class TimelineCreate(TimelineBase):
    pass

class TimelineOut(TimelineBase):
    id: int
    date: date

class TimelineUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: datetime.date | None = None

