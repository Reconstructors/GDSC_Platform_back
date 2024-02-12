from sqlalchemy.orm import Session

from ..models import introduction_models
from ..schemas import introduction_schemas


def get_timelines(db: Session, count: int = 1):
    db_timelines = db.query(introduction_models.Timeline).order_by(
        introduction_models.Timeline.date.desc()).limit(count).all()
    return list(map(introduction_schemas.Timeline.from_orm, db_timelines))


def create_timeline(db: Session, timeline: introduction_schemas.TimelineCreate):
    db_timeline = introduction_models.Timeline(
        title=timeline.title, date=timeline.date)
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline


def update_timeline(db: Session, timeline_id: int, timeline_update: introduction_schemas.TimelineUpdate):
    db_timeline = db.query(introduction_models.Timeline).filter(introduction_models.Timeline.id == timeline_id).first()
    if not db_timeline:
        return None
    update_data = timeline_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_timeline, key, value)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline

def delete_timeline(db: Session, timeline_id: int):
    db_timeline = db.query(introduction_models.Timeline).filter(introduction_models.Timeline.id == timeline_id).first()
    if not db_timeline:
        return None
    db.delete(db_timeline)
    db.commit()
    return db_timeline