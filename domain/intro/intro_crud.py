from datetime import datetime
from sqlalchemy.orm import Session

from models import Timeline  # 가정한 모델명, 실제 모델명에 맞춰서 변경 필요
from domain.intro.intro_schema import TimelineCreate, TimelineUpdate  # 가정한 스키마 경로 및 이름, 실제에 맞춰서 변경 필요

def get_timeline_list(db: Session, skip: int = 0, limit: int = 8):
    _timeline_list = db.query(Timeline).order_by(Timeline.date.desc())
    total = _timeline_list.count()
    timeline_list = _timeline_list.offset(skip).limit(limit).all()
    return total, timeline_list  # 전체 건수, 페이징 적용된 타임라인 목록

def get_timeline(db: Session, timeline_id: int):
    timeline = db.query(Timeline).get(timeline_id)
    return timeline

def create_timeline(db: Session, timeline_create: TimelineCreate):
    db_timeline = Timeline(
        title=timeline_create.title,
        date=datetime.now(),  # 타임라인 생성 날짜, 필요에 따라 timeline_create.date로 변경 가능
        description=timeline_create.description  # 예제에는 없지만 추가될 수 있는 필드
        # 기타 필요한 필드 추가
    )
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline

def update_timeline(db: Session, timeline_id: int, timeline_update: TimelineUpdate):
    db_timeline = db.query(Timeline).get(timeline_id)
    if db_timeline:
        db_timeline.title = timeline_update.title
        db_timeline.date = timeline_update.date  # 변경 가능한 필드
        db_timeline.description = timeline_update.description  # 예제에는 없지만 추가될 수 있는 필드
        # 기타 필요한 필드 업데이트
        db.commit()
        db.refresh(db_timeline)
        return db_timeline
    return None  # 타임라인이 존재하지 않는 경우

def delete_timeline(db: Session, timeline_id: int):
    db_timeline = db.query(Timeline).get(timeline_id)
    if db_timeline:
        db.delete(db_timeline)
        db.commit()
        return True
    return False  # 타임라인이 존재하지 않는 경우
