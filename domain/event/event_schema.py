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
    event_id: int


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True

class EventList(BaseModel):
    total: int = 0
    event_list: list[Event] = []

class EventDelete(BaseModel):
    event_id: int