from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Date, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from ..database import Base


class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 활동 제목
    date = Column(Date)  # 활동 일자
