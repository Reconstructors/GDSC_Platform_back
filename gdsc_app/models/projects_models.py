from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from ..database import Base

# 상태를 나타내는 Enum 클래스 정의
class ProjectStatus(PyEnum):
    PLANNING = "Planning"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    CANCELED = "Canceled"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 스터디 제목
    start = Column(DateTime)  # 프로젝트 시작 시간
    end = Column(DateTime, nullable=True)  # 프로젝트 종료 시간, null 허용
    description = Column(String)  # 프로젝트 소개
    contact_info = Column(JSON)  # 연락처 정보, JSON 형태의 문자열로 저장
    status = Column(String, Enum(ProjectStatus))  # 스터디 상태
    photo_ids = Column(JSON)  # 사진 ID 리스트, JSON 타입으로 저장
    member_ids = Column(JSON) # 프로젝트 구성원 ID 리스트