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

class TimelineUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime.date] = None