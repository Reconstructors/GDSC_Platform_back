from datetime import datetime
from sqlalchemy.orm import Session

from models import Timeline, User
from domain.timeline.timeline_schema import TimelineCreate, TimelineUpdate


# 타임라인 목록 반환
def get_timeline_list(db: Session, skip: int = 0, limit: int = 8):
    _timeline_list = db.query(Timeline).order_by(Timeline.date.desc())

    timeline_list = _timeline_list.offset(skip).limit(limit).all()
    return timeline_list  # 전체 건수, 페이징 적용된 타임라인 목록

# 특정 id를 가진 타임라인 반환
def get_timeline(db: Session, timeline_id: int):
    timeline = db.query(Timeline).get(timeline_id)
    return timeline

# 타임라인 생성
def create_timeline(db: Session, timeline_create: TimelineCreate, user_id: int):
    db_timeline = Timeline(
        title=timeline_create.title,
        date=timeline_create.date,
        description=timeline_create.description,
        user_id = user_id
    )
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline

def update_timeline(db: Session, timeline_update: TimelineUpdate, timeline_id: int):

    db_timeline = db.query(Timeline).get(timeline_id)

    

    update_data = timeline_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_timeline, key, value)

    

    db.commit()
    db.refresh(db_timeline)

    return db_timeline

def delete_timeline(db: Session, db_timeline: Timeline):
    db.delete(db_timeline)
    db.commit()