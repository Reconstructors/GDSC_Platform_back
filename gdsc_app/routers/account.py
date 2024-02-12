from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..services import account_crud
from ..schemas import account_schemas
from ..dependencies import get_db

router = APIRouter(tags=["Account"])

@router.post("/api/account/login/")
def login(token_data: account_schemas.JWTTokenData, db: Session = Depends(get_db)):
    user_info = account_crud.authenticate_user(token_data.token)
    print(token_data.token)
    if user_info:
        db_user = account_crud.get_user_by_email(db, email=user_info['email'])
        print(db_user)
        print("help")
        return {"message": "Token received and verified", "user_info": user_info}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/api/account/signup/")
def signup(user: account_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = account_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return account_crud.create_user(db=db, user=user)