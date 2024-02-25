from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from .database import engine, Base
from .routers import account, projects, studies, introduction, notice, event

Base.metadata.create_all(bind=engine) # sqlalchemy를 이용해 모델을 기반으로 데이터베이스 테이블 생성

app = FastAPI()

app.include_router(account.router)
app.include_router(projects.router)
app.include_router(studies.router)
app.include_router(introduction.router)
app.include_router(notice.router)
app.include_router(event.router)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your client URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}