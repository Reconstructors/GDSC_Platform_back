from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

from ..services import account_crud
from ..schemas import account_schemas
from ..dependencies import get_db

router = APIRouter()

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


@router.post("/account/login")
def login(token_data: account_schemas.TokenData, db: Session = Depends(get_db)):
    user_info = verify_google_oauth2_token(token_data.token)
    print(token_data.token)
    if user_info:
        db_user = account_crud.get_user_by_email(db, email=user_info['email'])
        print(db_user)
        print("help")
        return {"message": "Token received and verified", "user_info": user_info}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/account/signup")
def signup(user: account_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = account_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return account_crud.create_user(db=db, user=user)