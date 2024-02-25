from sqlalchemy.orm import Session

from ..models import notice_models
from ..schemas import notice_schemas


def get_notice(db: Session, notice_id: int):
    return (
        db.query(notice_models.Notice)
        .filter(notice_models.Notice.id == notice_id)
        .first()
    )


def get_all_notice(db: Session, skip: int = 0, limit: int = 8):
    return db.query(notice_models.Notice).offset(skip).limit(limit).all()

    # title: str
    # author_id: int
    # tag: Optional[List[str]] = []
    # upload_date: date
    # photo_ids: List[str] | None = []
    # content: str
    # view: int


def create_notice(db: Session, notice: notice_schemas.NoticeCreate):
    db_notice = notice_models.Notice(
        title=notice.title,
        author_id=notice.author_id,
        tag = notice.tag,
        upload_date=notice.upload_date,
        photo_ids=notice.photo_ids,
        content=notice.content,
        view=0,
    )
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice


def update_notice(
    db: Session, notice_id: int, notice_update: notice_schemas.NoticeUpdate
):
    db_notice = (
        db.query(notice_models.Notice)
        .filter(notice_models.Notice.id == notice_id)
        .first()
    )
    update_data = notice_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notice, key, value)
    db.commit()
    db.refresh(db_notice)
    return db_notice


def delete_notice(db: Session, notice_id: int):
    db_notice = (
        db.query(notice_models.Notice)
        .filter(notice_models.Notice.id == notice_id)
        .first()
    )
    if not db_notice:
        return None
    db.delete(db_notice)
    db.commit()
    return db_notice


def delete_all_notices(db: Session):
    try:
        db.query(notice_models.Notice).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error deleting notices: {e}")
        return False

    #     title: str
    # author_id: int
    # tag: List[str] | None = None
    # photo_ids: List[str] | None = []
    # content: str
    # id, view, upload_date
