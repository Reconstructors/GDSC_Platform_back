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
@router.get("/list", response_model=project_schema.ProjectList)
def project_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _project_list = project_crud.get_project_list(
        db, skip=page * size, limit=size
    )
    return {"total": total, "project_list": _project_list}


# id로 프로젝트 불러오기
@router.get("/detail/{project_id}", response_model=project_schema.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id=project_id)
    return project


@router.post("/create", status_code=status.HTTP_201_CREATED)  # 상태 코드 변경을 HTTP_204_NO_CONTENT에서 HTTP_201_CREATED로 수정
def project_create(
    _project_create: project_schema.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 프로젝트 생성
    new_project = project_crud.create_project(
        db=db, project_create=_project_create
    )
    
    # 프로젝트 생성자를 자동으로 매칭에 추가 (리더로 설정)
    project_crud.create_user_project_match(
        db=db, 
        user_id=current_user.id,  # 현재 사용자의 ID
        project_id=new_project.id,  # 새로 생성된 프로젝트의 ID
        is_approved=True,  # 승인된 매칭으로 설정
        is_leader=True  # 리더로 설정
    )

    return new_project  # 생성된 프로젝트 객체 반환



# id로 프로젝트 수정하기
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_project(
    _project_update: project_schema.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = project_crud.get_project(db, project_id=_project_update.project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다."
        )
    if current_user.id != db_project.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."
        )
    project_crud.update_project(
        db=db, db_project=db_project, project_update=_project_update
    )


# id로 프로젝트 삭제하기
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def project_delete(
    _project_delete: project_schema.ProjectDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = project_crud.get_project(db, project_id=_project_delete.project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다."
        )
    if not current_user.id != db_project.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )
    project_crud.delete_project(db=db, db_project=db_project)


@router.post(
    "/match",
    response_model=project_schema.UserProjectMatch,
    status_code=status.HTTP_201_CREATED,
)
def create_match(
    _match_create: project_schema.UserProjectMatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != _match_create.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자신의 ID로만 참여 신청이 가능합니다.",
        )
    return project_crud.create_user_project_match(
        db=db, user_id=_match_create.user_id, project_id=_match_create.project_id
    )


@router.delete("/match/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    _match_delete: project_schema.UserProjectMatchDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not project_crud.delete_user_project_match(
        db=db, user_id=_match_delete.user_id, project_id=_match_delete.project_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="매치를 찾을 수 없습니다."
        )
    return {"message": "매치가 성공적으로 삭제되었습니다."}

@router.get("/match/users/{project_id}", response_model=List[user_schema.User])
def read_users_for_project(project_id: int, db: Session = Depends(get_db)):
    users = project_crud.get_users_for_project(db, project_id=project_id)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    return users
