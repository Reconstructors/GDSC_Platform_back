from pydantic import BaseModel, Field, constr
from datetime import date


class Timeline(BaseModel):
    id: int
    title: str
    date: date

    class Config:
        from_attributes = True


class TimelineCreate(BaseModel):
    title: str
    date: date
