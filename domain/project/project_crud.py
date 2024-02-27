from datetime import datetime
from sqlalchemy.orm import Session

from models import Project, User
from domain.project.project_schema import ProjectCreate, ProjectUpdate


def get_project_list(db: Session, skip: int = 0, limit: int = 8):
    _project_list = db.query(Project).order_by(Project.create_date.desc())
    total = _project_list.count()
    project_list = _project_list.offset(skip).limit(limit).all()
    return total, project_list # 전체 건수, 페이징 적용된 프로젝트 목록

def get_project(db: Session, project_id: int):
    project = db.query(Project).get(project_id)
    return project

def create_project(db: Session, project_create: ProjectCreate, user=User):
    db_project = Project(
        title=project_create.title,
        create_date = datetime.now(),
        start=project_create.start,
        end=project_create.end,
        description=project_create.description,
        contact_info=project_create.contact_info,
        status=project_create.status,
        photo_ids=project_create.photo_ids,
        user = user
    )
    db.add(db_project)
    db.commit()

def update_project(db: Session, db_project: Project, project_update: ProjectUpdate):
    db_project.title = project_update.title
    db_project.description = project_update.description
    db_project.start = project_update.start
    db_project.end = project_update.end
    db_project.contact_info = project_update.contact_info
    db_project.photo_ids = project_update.photo_ids
    db_project.status = project_update.status
    db_project.modify_date = datetime.now()
    db.commit()

def delete_project(db: Session, db_project: Project):
    db.delete(db_project)
    db.commit()