from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500","http://localhost:5501"],  # Allows requests from your client URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define your Google OAuth2 client ID
CLIENT_ID = "902126570126-k61fod9mop3g2i3hh3r175fq4ba3gufa.apps.googleusercontent.com"

def verify_google_oauth2_token(token):
    try:
        # Specify the CLIENT_ID of your app
        userinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return userinfo
    except ValueError:
        # Invalid token
        return None


@app.post("/api/account/login")
def login(token_data: schemas.TokenData, db: Session = Depends(get_db)):
    user_info = verify_google_oauth2_token(token_data.token)
    print(token_data.token)
    if user_info:
        db_user = crud.get_user_by_email(db, email=user_info['email'])
        print(db_user)
        print("help")
        return {"message": "Token received and verified", "user_info": user_info}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/account/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#################################################################################

@app.post("/api/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.get("/api/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

#################################################################################

@app.post("/api/studies/", response_model=schemas.Study)
def create_study(study: schemas.StudyCreate, db: Session = Depends(get_db)):
    return crud.create_study(db=db, study=study)

@app.get("/api/studies/{study_id}", response_model=schemas.Study)
def read_study(study_id: int, db: Session = Depends(get_db)):
    db_study = crud.get_study(db, study_id=study_id)
    if db_study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return db_study

@app.post("/api/study_matches/", response_model=schemas.StudyMatch)
def create_study_match_endpoint(study_match: schemas.StudyMatchCreate, db: Session = Depends(get_db)):
    return crud.create_study_match(db=db, study_match=study_match)

@app.get("/api/study_matches/{match_id}", response_model=schemas.StudyMatch)
def read_study_match(match_id: int, db: Session = Depends(get_db)):
    db_study_match = crud.get_study_match(db, match_id=match_id)
    if db_study_match is None:
        raise HTTPException(status_code=404, detail="Study match not found")
    return db_study_match

@app.get("/api/study_matches/", response_model=List[schemas.StudyMatch])
def read_study_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    study_matches = crud.get_study_matches(db, skip=skip, limit=limit)
    return study_matches