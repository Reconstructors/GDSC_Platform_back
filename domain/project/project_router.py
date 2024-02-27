from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from domain.project import project_schema, project_crud
from domain.user.user_router import get_current_user
from models import User
from database import get_db

router = APIRouter(prefix="/api/project", tags=["Project"])

# 프로젝트 목록 불러오기
@router.get("/list", response_model=List[project_schema.ProjectList])
def project_list(db: Session = Depends(get_db), page: int=0, size: int=10):
    total, _project_list = project_crud.get_project_list(
        db, skip=page*size, limit=size
    )
    return {
        'total': total,
        'project_list': _project_list
    }

# id로 프로젝트 불러오기
@router.get("/detail/{project_id}", response_model=project_schema.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id=project_id)
    return project

# 프로젝트 생성하기
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def project_create(_project_create: project_schema.ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project_crud.create_project(db=db, project_create=_project_create, user=current_user)

# id로 프로젝트 수정하기
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_project(_project_update: project_schema.ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = project_crud.get_project(db, project_id=_project_update.project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_project.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    project_crud.update_project(db=db, db_project=db_project,
                                project_update=_project_update)

# id로 프로젝트 삭제하기
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def project_delete(_project_delete: project_schema.ProjectDelete, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = project_crud.get_project(db, project_id=_project_delete.project_id)
    if not db_project:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    if not current_user.id != db_project.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    project_crud.delete_project(db=db, db_project=db_project)