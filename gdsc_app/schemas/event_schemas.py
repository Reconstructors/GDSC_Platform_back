from pydantic import BaseModel, Field, constr
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum


class EventBase(BaseModel):
    title: str
    start: date
    end: Optional[date] = None
    cohort: int
    status: str
    photo_id: str | None = None
    location: str


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True
