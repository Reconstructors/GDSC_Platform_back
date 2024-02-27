from pydantic import BaseModel, Field, constr
from typing import List, Tuple, Optional
from datetime import date
from enum import Enum

class NoticeBase(BaseModel):
    title: str
    author_id: int
    tag: List[str] | None = []
    upload_date: date
    photo_ids: List[str] | None = []
    content: str
    view: int

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(NoticeBase):
    pass

class Notice(NoticeBase):
    id: int

    class Config:
        from_attributes = True