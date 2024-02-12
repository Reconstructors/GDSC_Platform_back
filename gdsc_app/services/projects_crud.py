from sqlalchemy.orm import Session

from ..models import projects_models
from ..schemas import projects_schemas


def get_projects(db: Session, skip: int = 0, limit: int = 8):
    return db.query(projects_models.Project).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(projects_models.Project).filter(projects_models.Project.id == project_id).first()

def create_project(db: Session, project: projects_schemas.ProjectCreate):
    db_project = projects_models.Project(
        title=project.title,
        start=project.start,
        end=project.end,
        description=project.description,
        contact_info=project.contact_info,
        status=project.status,
        photo_ids=project.photo_ids
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project_update: projects_schemas.ProjectUpdate):
    db_project = db.query(projects_models.Project).filter(projects_models.Project.id == project_id).first()
    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id:int):
    db_project = db.query(projects_models.Project).filter(projects_models.Project.id == project_id).first()
    if not db_project:
        return None
    db.delete(db_project)
    db.commit()
    return db_project