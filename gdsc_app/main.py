from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import account, projects, studies, introduction

Base.metadata.create_all(bind=engine) # sqlalchemy를 이용해 모델을 기반으로 데이터베이스 테이블 생성

app = FastAPI()

app.include_router(account.router)
app.include_router(projects.router)
app.include_router(studies.router)
app.include_router(introduction.router)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your client URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)