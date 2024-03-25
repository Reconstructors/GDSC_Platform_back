from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.study import study_schema, study_crud
from domain.user import user_crud, user_schema
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
@router.get("/list", response_model=list[study_schema.StudyOut])
def study_list(page: int = 0, size: int = 10, db: Session = Depends(get_db)):
    """
    스터디 목록 얻기

    이 API는 승인든 스터디 참가자의 id 목록과 함께 스터디 목록을 반환합니다.
    """
    _study_list = study_crud.get_study_list(db, skip=page * size, limit=size)
    result = []
    for study in _study_list:
        participants_ids = study_crud.get_approved_user_ids_by_study_id(db=db,study_id=study.id)
        study_dict = model_to_dict(study)
        # Study 인스턴스를 StudyOut 스키마에 맞게 변환
        study_data = study_schema.StudyOut(**study_dict, people=participants_ids)
        result.append(study_data)
    return result


# study id로 스터디 정보, 참가자 정보 불러오기
@router.get("/detail/{study_id}")
def study_detail(study_id: int, db: Session = Depends(get_db)):
    """
    단일 스터디 정보 얻기

    이 API는 study id에 해당하는 스터디의 정보를 승인된 참가자의 정보와 함께 반환합니다.
    스터디 참가자는 스터디 개설자도 포함하며, "study" key 항목의 owner_id를 통해서 확인할 수 있습니다.

    study id에 해당하는 스터디가 존재하지 않을 경우, 404 에러를 반환합니다.
    """
    study = study_crud.get_study(db, study_id=study_id)

    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    user_id_list = study_crud.get_approved_user_ids_by_study_id(db=db, study_id=study_id)
    user_objects = user_crud.get_users_by_id_list(db=db ,user_id_list=user_id_list)

    user_list = [user_schema.UserOut.model_validate(user, from_attributes=True) for user in user_objects]

    return {
        "study": study,
        "participants": user_list
        }


# 스터디 생성하기
@router.post("/create", status_code=status.HTTP_201_CREATED)
def study_create(
    _study_create: study_schema.StudyCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    스터디 생성하기

    이 API는 스터디를 생성합니다.\n
    스터디 개설자는 자동으로 스터디에 참여하게 됩니다.\n
    """
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

# 스터디 수정하기
@router.patch("/update/{study_id}", status_code=status.HTTP_200_OK)
def study_update(
    study_id: int,
    study_update: study_schema.StudyUpdate,
    user_id: User = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    스터디 정보 수정하기

    이 API는 스터디 정보를 수정합니다.\n
    수정은 스터디 개설자만 가능합니다.\n

    존재하지 않는 스터디일 경우 404에러를, 수정 권한이 없는 사용자의 경우 400 에러를 반환합니다.    
    """
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

# 스터디 삭제하기
@router.delete("/delete/{study_id}", status_code=status.HTTP_204_NO_CONTENT)
def study_delete(
    study_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    스터디 삭제하기

    이 API는 스터디를 삭제합니다\n
    삭제는 스터디 개설자만 가능합니다.\n

    존재하지 않는 스터디일 경우 404에러를, 삭제 권한이 없는 사용자의 경우 400 에러를 반환합니다.    
    """
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


# 스터디 신청하기
@router.post("/apply/{study_id}")
def study_apply(
    study_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    스터디 신청하기

    이 API는 스터디 참가 신청을 합니다.\n
    삭제는 스터디 개설자만 가능합니다.\n

    존재하지 않는 스터디일 경우 404에러를, 이미 스터디를 신청한 유저인 경우 409에러를 반환합니다.
    """

    db_study = study_crud.get_study(db=db, study_id=study_id)
    if db_study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found."
        )
    
    existing_match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=user_id)
    if existing_match:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User has already applied to this study."
        )
    
    study_match_create = study_schema.StudyMatchCreate(
        user_id=user_id,
        study_id=study_id,
        is_approved=False,  # 스터디 참여 희망자이므로 승인 상태를 False로 설정
        is_leader=False
    )

    # 스터디 매치 생성
    study_crud.create_study_match(db=db, study_match_create=study_match_create)
    return {"msg": "study application created successfully."}
    
# 스터디 참가 신청자 목록 반환하기
# - 스터디 개설자만 요청 가능
@router.post("/{study_id}/apply-list")
def user_application_list(study_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    스터디 참가 신청자 정보 얻기

    이 API는 승인 여부에 관계없이 스터디에 대한 모든 참가 신청자에 대한 정보를 반환합니다. \n
    스터디 개설자만 요청 가능합니다.\n

    존재하지 않는 스터디일 경우 404에러를, 요청 권한이 없는 경우(스터디 개설자가 아닌 경우) 401에러를 반환합니다.
    """

    # 스터디 존재 여부 확인
    db_study = study_crud.get_study(db=db, study_id=study_id)
    if db_study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )
    
    # 스터디 개설자 확인
    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=user_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )
    elif match.is_leader == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Only leader can get unapproved user list"
        )

    user_info = []
    match_list = study_crud.get_study_matches_by_study_id(db=db, study_id=study_id, only_approved=False, only_unapproved=False)
    for match in match_list:
        user = user_crud.get_user_by_id(db=db, user_id=match.user_id)

        user_dict = user_schema.UserOut.model_validate(user, from_attributes=True).model_dump()

        user_dict["is_approved"] = match.is_approved
        user_dict["is_leader"] = match.is_leader

        user_out = study_schema.StudyMatchWithUserInfo.model_validate(user_dict, from_attributes=True)
        user_info.append(user_out)
    return user_info


# 스터디 참가 요청 승인 or 비승인으로 전환
# FIXME: user_id 전달 방식 이게 최선인가
@router.patch("/{study_id}/apply/{applicant_id}")
def approve_or_disapprove_user(
        study_id: int, 
        applicant_id: int,
        approved: bool,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    
    """
    스터디 신청자 승인 or 비승인 전환하기

    이 API는 스터디 참가 신청자에 대해서 승인 또는 승인에서 비승인으로 전환을 합니다\n
    요청은 스터디 개설자만 가능하며, approved 값이 True면 승인, False면 승인에서 비승인으로 전환입니다.\n

    요청이 성공할 경우, 수정된 match 정보를 반환합니다.\n

    존재하지 않는 스터디일 경우 404에러를, 요청 권한이 없는 경우 401에러를 반환합니다.
    """

    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=user_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Study not found"
        )
    # 요청한 유저가 스터디 개설자인지 확인
    elif match.is_leader != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail= "Only leader can modify study match status"
        )

    match_db = study_crud.change_study_match_staus(db=db, study_id=study_id, user_id=applicant_id, approved=approved)
    return {
        "msg": "change match status success",
        "result": match_db
        }
        
# TODO: 스터디 참여 요청 거절하기
#   - 스터디를 만든 사람만 요청 가능
# FIXME: DB 수정이 필요해 보임

# 스터디 탈퇴 or 신청 취소
@router.delete("/quit/{study_id}")
def quit_study(
        study_id: int, 
        user_id: int = Depends(get_current_user_id), 
        db: Session = Depends(get_db)):
    """
    스터디 탈퇴 or 신청 취소하기

    이 API는 스터디 참가자나 신청자에 대해 탈퇴 처리를 합니다.\n
    요청은 스터디 신청자 혹은 참여자만 가능하며, 스터디 개설자는 요청이 불가능합니다.\n

    존재하지 않는 스터디일 경우 404에러를, 요청 권한이 없는 경우 401에러를 반환합니다.\n
    스터디 개설자가 요청할 경우 400에러를 반환합니다.
    """
    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=user_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )

    if match.is_leader == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Study leader cannot quit study"
        )

    study_crud.delete_study_match(match)
    return {"msg": "successfully left the study"}

# 스터디 리더 변경하기
@router.post("/study/leader/{study_id}")
def change_study_leader(
        study_id: int,
        next_leader_id: int,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    """
    스터디 리더 변경하기

    이 API는 스터디 참가자 중 한 사람에게 리더 권한을 넘깁니다.\n
    요청은 스터디 리더만 가능하며, 스터디 참가에 승인된 유저에게만 리더 권한을 부여할 수 있습니다.\n
    요청이 성공할 시, 요청자는 리더 권한을 잃게 됩니다.

    존재하지 않는 스터디일 경우 404에러를, 요청 권한이 없는 경우 401에러를 반환합니다.\n
    """
    match = study_crud.get_study_match_by_study_id_user_id(db=db, study_id=study_id, user_id=user_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )

    if match.is_leader != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Only leader can change study leader"
        )
    
    study_crud.change_study_leader(db=db, study_id=study_id, original_leader_id=user_id, next_leader_id=next_leader_id)
    return {"msg": "successfully changed the study leader"}