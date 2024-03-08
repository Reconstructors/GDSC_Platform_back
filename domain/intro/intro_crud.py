from datetime import datetime
from sqlalchemy.orm import Session

from models import Timeline, User
from domain.intro.intro_schema import TimelineCreate, TimelineUpdate

def get_timeline_list(db: Session, skip: int = 0, limit: int = 8):
    _timeline_list = db.query(Timeline).order_by(Timeline.date.desc())
    total = _timeline_list.count()
    timeline_list = _timeline_list.offset(skip).limit(limit).all()
    return total, timeline_list  # 전체 건수, 페이징 적용된 타임라인 목록

def get_timeline(db: Session, timeline_id: int):
    timeline = db.query(Timeline).get(timeline_id)
    return timeline

def create_timeline(db: Session, timeline_create: TimelineCreate, user=User):
    db_timeline = Timeline(
        title=timeline_create.title,
        date=datetime.now(),  # 타임라인 생성 날짜, 필요에 따라 timeline_create.date로 변경 가능
        description=timeline_create.description,
        # 기타 필요한 필드 추가
        user = user
    )
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline

def update_timeline(db: Session, db_timeline: Timeline, timeline_update: TimelineUpdate):
    db_timeline.title = timeline_update.title
    db_timeline.description = timeline_update.description
    db_timeline.date = timeline_update.date
    db.commit()

def delete_timeline(db: Session, db_timeline: Timeline):
    db.delete(db_timeline)
    db.commit()