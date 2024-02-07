from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..services import projects_crud
from ..schemas import projects_schemas
from ..dependencies import get_db

router = APIRouter(tags=["Project"])

@router.post("/projects/", response_model=projects_schemas.Project)
def create_project(project: projects_schemas.ProjectCreate, db: Session = Depends(get_db)):
    return projects_crud.create_project(db=db, project=project)

@router.get("/projects/{project_id}", response_model=projects_schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project