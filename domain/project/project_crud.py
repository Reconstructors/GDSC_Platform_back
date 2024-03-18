# from datetime import datetime
# from sqlalchemy.orm import Session

# from models import Project, User, UserProjectMatch
# from domain.project.project_schema import ProjectCreate, ProjectUpdate


# def get_project_list(db: Session, skip: int = 0, limit: int = 8):
#     _project_list = db.query(Project).order_by(Project.create_date.desc())
#     total = _project_list.count()
#     project_list = _project_list.offset(skip).limit(limit).all()
#     return total, project_list  # 전체 건수, 페이징 적용된 프로젝트 목록


# def get_project(db: Session, project_id: int):
#     project = db.query(Project).get(project_id)
#     return project


# def get_projects_for_user(db: Session, user_id: int):
#     projects = (
#         db.query(Project)
#         .join(UserProjectMatch, Project.id == UserProjectMatch.project_id)
#         .filter(UserProjectMatch.user_id == user_id)
#         .all()
#     )
#     return projects

# def get_users_for_project(db: Session, project_id: int):
#     users = db.query(User).join(UserProjectMatch, User.id == UserProjectMatch.user_id).filter(UserProjectMatch.project_id == project_id).all()
#     return users

# def create_project(db: Session, project_create: ProjectCreate):
#     # Project 인스턴스 생성
#     db_project = Project(
#         title=project_create.title,
#         create_date=datetime.now(),
#         start=project_create.start,
#         end=project_create.end,
#         description=project_create.description,
#         contact_info=project_create.contact_info,
#         status=project_create.status,
#         photo_ids=project_create.photo_ids,
#     )
#     db.add(db_project)
#     db.commit()
#     return db_project


# def create_user_project_match(db: Session, user_id: int, project_id: int):
#     db_user_project_match = UserProjectMatch(
#         user_id=user_id, project_id=project_id, is_approved=True, is_leader=True
#     )
#     db.add(db_user_project_match)
#     db.commit()
#     db.refresh(db_user_project_match)
#     return db_user_project_match


# def update_project(db: Session, db_project: Project, project_update: ProjectUpdate):
#     db_project.title = project_update.title
#     db_project.description = project_update.description
#     db_project.start = project_update.start
#     db_project.end = project_update.end
#     db_project.contact_info = project_update.contact_info
#     db_project.photo_ids = project_update.photo_ids
#     db_project.status = project_update.status
#     db_project.modify_date = datetime.now()
#     db.commit()

# def update_user_project_match(db: Session, user_id: int, project_id: int, is_approved: bool = None, is_leader: bool = None):
#     match = db.query(UserProjectMatch).filter(UserProjectMatch.user_id == user_id, UserProjectMatch.project_id == project_id).first()
#     if match is not None:
#         if is_approved is not None:
#             match.is_approved = is_approved
#         if is_leader is not None:
#             match.is_leader = is_leader
#         db.commit()
#         db.refresh(match)
#     return match



# def delete_project(db: Session, db_project: Project):
#     db.delete(db_project)
#     db.commit()

# def delete_user_project_match(db: Session, user_id: int, project_id: int):
#     match = db.query(UserProjectMatch).filter(UserProjectMatch.user_id == user_id, UserProjectMatch.project_id == project_id).first()
#     if match:
#         db.delete(match)
#         db.commit()
#         return True
#     return False
