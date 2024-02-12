from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    bio = Column(String, index=True)  # 한 줄 소개
    description = Column(String)  # 자세한 자기소개
    links = Column(String)  # JSON 형태의 문자열로 저장
    interests = Column(JSON)  # 관심분야, list 타입으로 저장
    participation = Column(JSON)  # 참여 기수 및 직위, list 타입으로 저장
    project_interest = Column(Boolean)  # 프로젝트 참여 희망 여부
    study_matches = relationship("StudyMatch", back_populates="user")