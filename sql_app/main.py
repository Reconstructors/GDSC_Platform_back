from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

########################### 실제 사용 코드 #######################################
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google.oauth2 import id_token
from google.auth.transport import requests

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Allows requests from your client URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenData(BaseModel):
    token: str = Field()

# Define your Google OAuth2 client ID
CLIENT_ID = "902126570126-k61fod9mop3g2i3hh3r175fq4ba3gufa.apps.googleusercontent.com"
#CLIENT_ID = "902126570126-58tn16k8uiuegrcborbcdumiiskk6f9p"

def verify_google_oauth2_token(token):
    try:
        # Specify the CLIENT_ID of your app
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userinfo = idinfo
        return userinfo
    except ValueError:
        # Invalid token
        return None


@app.post("/api/account/login")
def login(token_data: TokenData):
    user_info = verify_google_oauth2_token(token_data.token)
    print(token_data.token)
    if user_info:
        print(user_info)
        return {"message": "Token received and verified", "user_info": user_info}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

