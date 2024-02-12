from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship

from ..database import Base

class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 스터디 제목
    start = Column(DateTime)  # 스터디 시작 시간
    end = Column(DateTime, nullable=True)  # 스터디 종료 시간, null 허용
    description = Column(String)  # 스터디 소개
    contact_info = Column(JSON)  # 연락처 정보, JSON 형태의 문자열로 저장
    status = Column(String)  # 스터디 상태
    photo_ids = Column(JSON)  # 사진 ID 리스트, JSON 타입으로 저장
    study_matches = relationship("StudyMatch", back_populates="study")

class StudyMatch(Base):
    __tablename__ = "study_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # 유저 ID, 유저 테이블에 대한 외래 키
    study_id = Column(Integer, ForeignKey('studies.id'))  # 스터디 ID, 스터디 테이블에 대한 외래 키
    is_approved = Column(Boolean, default=False)  # 승인 여부, 기본값은 False
    is_leader = Column(Boolean, default=False)  # 스터디 팀장 여부, 기본값은 False

    user = relationship("User", back_populates="study_matches")
    study = relationship("Study", back_populates="study_matches")