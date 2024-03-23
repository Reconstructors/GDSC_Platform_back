from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.study import study_schema, study_crud
from domain.user import user_crud
from database import get_db
from models import User, UserStudyMatch
import datetime

from domain.auth.dependencies import get_current_user_id

router = APIRouter(tags=["Study"], prefix="/api/study")

def model_to_dict(model):
    return {
        column.name: (getattr(model, column.name).date() if isinstance(getattr(model, column.name), datetime.datetime) else getattr(model, column.name))
        for column in model.__table__.columns
    }

# 스터디 목록 불러오기
# FIXME: 승인 여부에 관계없이 people에 user가 포함되는 문제 해결 필요
@router.get("/list", response_model=list[study_schema.StudyOut])
def study_list(page: int = 0, size: int = 10, db: Session = Depends(get_db)):
    _study_list = study_crud.get_study_list(db, skip=page * size, limit=size)
    result = []
    for study in _study_list:
        participants_ids = study_crud.get_user_ids_by_study_id(db=db,study_id=study.id)
        study_dict = model_to_dict(study)
        # Study 인스턴스를 StudyOut 스키마에 맞게 변환
        study_data = study_schema.StudyOut(**study_dict, people=participants_ids)
        result.append(study_data)
    return result


# id로 스터디 불러오기
# TODO: 스터디 참여자 id 목록도 함께 반환
# DONE: id 목록인 아닌 매칭 정보 전체 반환
@router.get("/detail/{study_id}")
# , response_model=study_schema.Study
def study_detail(study_id: int, db: Session = Depends(get_db)):
    study = study_crud.get_study(db, study_id=study_id)
    matches = study_crud.get_study_matches_by_study_id(db=db, study_id=study.id)
    return study, matches


# 스터디 생성하기
@router.post("/create", status_code=status.HTTP_201_CREATED)
def study_create(
    _study_create: study_schema.StudyCreate,
    db: Session = Depends(get_db),
    user_id: User = Depends(get_current_user_id),
):

    db_study = study_crud.create_study(
        db=db, study_create=_study_create, user_id=user_id
    )
    # 스터디 생성자는 자연스럽게 스터디 가입
    study_match_create = study_schema.StudyMatchCreate(
        user_id=user_id,
        study_id=db_study.id,  # create_study에서 반환된 스터디 객체의 ID 사용
        is_approved=True,  # 스터디 생성자이므로 승인 상태를 True로 설정
        is_leader=True  # 스터디 생성자이므로 리더 상태를 True로 설정
    )

    # 스터디 매치 생성
    study_crud.create_study_match(db=db, study_match_create=study_match_create)
    return db_study


@router.patch("/update/{study_id}", status_code=status.HTTP_200_OK)
def study_update(
    study_id: int,
    study_update: study_schema.StudyUpdate,
    user_id: User = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):

    db_study = study_crud.get_study(db, study_id=study_id)
    if not db_study:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Study not found"
        )
    if user_id != db_study.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Permission denied"
        )

    return study_crud.update_study(db=db, db_study=db_study, study_update=study_update)

@router.delete("/delete/{study_id}", status_code=status.HTTP_204_NO_CONTENT)
def study_delete(
    study_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    # 스터디 가져오기
    db_study = study_crud.get_study(db, study_id=study_id)
    if not db_study:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found."
        )
    # 사용자가 스터디의 소유자인지 확인
    if user_id != db_study.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this study."
        )
    # 스터디에 속한 모든 UserStudyMatch 인스턴스 반드시 삭제
    study_crud.delete_study_matches_by_study_id(db=db, study_id=study_id)
    # 스터디 삭제
    study_crud.delete_study(db=db, db_study=db_study)
    return {"msg": "Study deleted successfully."}


# DONE: 스터디 신청하기
@router.post("/register/{study_id}")
def study_register(
    study_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    study_match_create = study_schema.StudyMatchCreate(
        user_id=user_id,
        study_id=study_id,  # create_study에서 반환된 스터디 객체의 ID 사용
        is_approved=False,  # 스터디 참여 희망자이므로 승인 상태를 False로 설정
        is_leader=False
    )
    # 스터디 매치 생성
    study_crud.create_study_match(db=db, study_match_create=study_match_create)
    return {"msg": "study match created successfully."}
    
# TODO: 스터디 신청한 사용자 정보 리스트 반환하기
#   - 스터디를 만든 사람만 요청 가능
@router.get("/{study_id}/register-list")
def unapproved_user_list(study_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=user_id)
    if match.is_leader == True:
        user_info = []
        unapproved_user_ids = study_crud.get_unapproved_user_ids_by_study_id(db=db, study_id=study_id)
        for user_id in unapproved_user_ids:
            user_info.append(user_crud.get_user_by_id(db=db, user_id=user_id))
        return user_info
    return {"msg": "Only leader can get unapproved user list"}

# Done: 스터디 참여 요청 승인하기
#   - 스터디를 만든 사람만 요청 가능
# FIXME: user_id 전달 방식 이게 최선인가
@router.patch("/{study_id}/{user_id}/approve-user")
def approve_user(study_id: int, user_id:int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=current_user_id)
    if match.is_leader == True:
        match_db = study_crud.approve_study_match(db=db, study_id=study_id, user_id=user_id)
        return match_db
    return {"msg": "Only leader can do it!"}
    
# TODO: 스터디 참여 요청 거절하기
#   - 스터디를 만든 사람만 요청 가능
# FIXME: DB 수정이 필요해 보임

# TODO: 스터디 탈퇴하기
@router.delete("/{study_id}/leave")
def delete_match(study_id: int, user_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=current_user_id)
    study_crud.delete_study_match(match)
    return {"msg": "successfully leaved the study"}

# TODO: 스터디 리더 변경하기