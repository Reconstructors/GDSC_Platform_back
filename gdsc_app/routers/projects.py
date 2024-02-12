from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import projects_crud
from ..schemas import projects_schemas
from ..models import projects_models
from ..dependencies import get_db

router = APIRouter(tags=["Project"])

# 프로젝트 목록 불러오기
@router.get("/api/projects", response_model=List[projects_schemas.Project])
def read_project(skip: int = 0, limit: int=8, db: Session = Depends(get_db)):
    return projects_crud.get_projects(db=db, skip=skip, limit=limit)

# id로 프로젝트 불러오기
@router.get("/api/projects/{project_id}", response_model=projects_schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

# 프로젝트 생성하기
@router.post("/api/projects/", response_model=projects_schemas.Project)
def create_project(project: projects_schemas.ProjectCreate, db: Session = Depends(get_db)):
    return projects_crud.create_project(db=db, project=project)

# id로 프로젝트 수정하기
@router.patch("/api/projects/{project_id}", response_model=projects_schemas.Project)
def update_project(project_id: int, project_update: projects_schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(projects_models.Project).filter(projects_models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project_update.title is not None:
        db_project.title = project_update.title
    if project_update.start is not None:
        db_project.start = project_update.start
    db.commit()
    db.refresh(db_project)
    return db_project

# id로 프로젝트 삭제하기
@router.delete("/api/projects/{project_id}",response_model=projects_schemas.Project)
def delete_project(project_id: int, db: Session=Depends(get_db)):
    deleted_project = projects_crud.delete_project(db=db, project_id=project_id)
    if deleted_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return deleted_project