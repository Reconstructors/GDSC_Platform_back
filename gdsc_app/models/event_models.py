from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship

from ..database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start = Column(DateTime)  # 스터디 시작 시간
    end = Column(DateTime, nullable=True)  # 스터디 종료 시간, null 허용
    cohort = Column(Integer, index=True)  # 동아리 기수
    status = Column(String)  # Done ongoing upcoming
    type = Column(String)  # Regular, General,In campus, out campus
    photo_id = Column(String)
    location = Column(String)