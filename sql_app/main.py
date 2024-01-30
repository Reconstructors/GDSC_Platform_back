from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import account, projects, studies

Base.metadata.create_all(bind=engine) # sqlalchemy를 이용해 모델을 기반으로 데이터베이스 테이블 생성

app = FastAPI()

app.include_router(account.router)
app.include_router(projects.router)
app.include_router(studies.router)

# CORS Middleware 거지같은 CORS 문제 해결
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500","http://localhost:5501"],  # Allows requests from your client URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)