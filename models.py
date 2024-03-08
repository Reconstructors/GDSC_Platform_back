from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Enum, Date, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    cohort = Column(Integer, index=True,nullable=True)  # 동아리 기수
    position = Column(String, index=True, nullable=True) # core, member, leader
    bio = Column(String, nullable=True)  # 한 줄 소개
    description = Column(Text, nullable=True)  # 자세한 자기소개
    links = Column(JSON, nullable=True)  # JSON 형태의 문자열로 저장
    skills = Column(JSON, nullable=True)  # 스킬셋, list 타입으로 저장
    interests = Column(JSON, nullable=True)  # 관심분야, list 타입으로 저장
    project_interest = Column(Boolean, nullable=True)  # 프로젝트 참여 희망 여부

# 상태를 나타내는 Enum 클래스 정의
class ProjectStatus(PyEnum):
    PLANNING = "Planning"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    CANCELED = "Canceled"


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 프로젝트 제목
    start = Column(Date)  # 프로젝트 시작 시간
    end = Column(Date, nullable=True)  # 프로젝트 종료 시간, null 허용
    description = Column(Text)  # 프로젝트 소개
    contact_info = Column(JSON)  # 연락처 정보, JSON 형태의 문자열로 저장
    status = Column(String, Enum(ProjectStatus))  # 스터디 상태
    photo_ids = Column(JSON)  # 사진 ID 리스트, JSON 타입으로 저장
    create_date = Column(DateTime, nullable=True)
    modify_date = Column(DateTime, nullable=True)

class UserProjectMatch(Base):
    __tablename__ = "user_project_match"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # 유저 ID, 유저 테이블에 대한 외래 키
    project_id = Column(Integer, ForeignKey('project.id'))  # 스터디 ID, 스터디 테이블에 대한 외래 키
    is_approved = Column(Boolean, default=False)  # 승인 여부, 기본값은 False
    is_leader = Column(Boolean, default=False)  # 팀장 여부, 기본값은 False

    user = relationship("User", backref="projects")
    study = relationship("Project", backref="users")


class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 스터디 제목
    start = Column(DateTime)  # 스터디 시작 시간
    end = Column(DateTime, nullable=True)  # 스터디 종료 시간, null 허용
    description = Column(String)  # 스터디 소개
    contact_info = Column(JSON)  # 연락처 정보, JSON 형태의 문자열로 저장
    status = Column(String)  # 스터디 상태
    photo_ids = Column(JSON)  # 사진 ID 리스트, JSON 타입으로 저장
    create_date = Column(DateTime, nullable=True)
    modify_date = Column(DateTime, nullable=False)

class UserStudyMatch(Base):
    __tablename__ = "user_study_match"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # 유저 ID, 유저 테이블에 대한 외래 키
    study_id = Column(Integer, ForeignKey('study.id'))  # 스터디 ID, 스터디 테이블에 대한 외래 키
    is_approved = Column(Boolean, default=False)  # 승인 여부, 기본값은 False
    is_leader = Column(Boolean, default=False)  # 스터디 팀장 여부, 기본값은 False

    user = relationship("User", backref="studies")
    study = relationship("Study", backref="users")


# class Notice(Base):
#     __tablename__ = "notice"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True) 
#     tag = Column(JSON)
#     upload_date = Column(Date)
#     view = Column(Integer)
#     photo_ids = Column(JSON)
#     content = Column(String)
#     user_id = Column(Integer, ForeignKey("user"))
#     user = relationship("User", backref="notice_users")
#     modify_date = Column(DateTime, nullable=True)


# class Event(Base):
#     __tablename__ = "events"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     start = Column(DateTime)  # 스터디 시작 시간
#     end = Column(DateTime, nullable=True)  # 스터디 종료 시간, null 허용
#     status = Column(String)  # Done ongoing upcoming
#     type = Column(String)  # Regular, General,In campus, out campus
#     photo_id = Column(String)
#     location = Column(String)
#     user_id = Column(Integer, ForeignKey("user"))
#     user = relationship("User", backref="event_users")
#     modify_date = Column(DateTime, nullable=True)


class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 활동 제목
    description = Column(Text)
    date = Column(Date)  # 활동 일자
    user_id = Column(Integer, ForeignKey('user.id'))  # 유저 ID, 유저 테이블에 대한 외래 키
    user = relationship("User", backref="timelines")









