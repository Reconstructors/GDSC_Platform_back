from datetime import datetime
from sqlalchemy.orm import Session

from models import Notice, User  # 모델 경로 가정
from domain.notice.notice_schema import NoticeCreate, NoticeUpdate  # 스키마 경로 가정

def get_notice_list(db: Session, skip: int = 0, limit: int = 100):
    _notice_list = db.query(Notice).order_by(Notice.upload_date.desc())
    total = _notice_list.count()
    notice_list = _notice_list.offset(skip).limit(limit).all()
    return total, notice_list  # 전체 건수, 페이징 적용된 공지사항 목록

def get_notice(db: Session, notice_id: int):
    notice = db.query(Notice).get(notice_id)
    return notice

def create_notice(db: Session, notice_create: NoticeCreate, user=User):
    db_notice = Notice(
        title=notice_create.title,
        author_id=user.id,  # User 모델의 id를 사용, 사용자 인증/식별 방식에 따라 변경 가능
        tag=notice_create.tag,
        upload_date=datetime.now(),
        photo_ids=notice_create.photo_ids,
        content=notice_create.content,
        view=0  # 조회수는 새 공지사항 생성 시 0으로 초기화
    )
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice

def update_notice(db: Session, notice_id: int, notice_update: NoticeUpdate):
    db_notice = db.query(Notice).get(notice_id)
    if db_notice:
        db_notice.title = notice_update.title
        db_notice.tag = notice_update.tag
        db_notice.upload_date = datetime.now()  # 수정 일자를 현재 시각으로 업데이트
        db_notice.photo_ids = notice_update.photo_ids
        db_notice.content = notice_update.content
        db_notice.view = notice_update.view  # 선택적으로 조회수도 업데이트할 수 있음
        db.commit()
        db.refresh(db_notice)
        return db_notice
    return None  # 공지사항이 존재하지 않는 경우

def delete_notice(db: Session, notice_id: int):
    db_notice = db.query(Notice).get(notice_id)
    if db_notice:
        db.delete(db_notice)
        db.commit()
        return True
    return False
