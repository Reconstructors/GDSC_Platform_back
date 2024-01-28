from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session

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