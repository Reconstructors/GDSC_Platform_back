from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# # from domain.event import event_router
from domain.timeline import timeline_router
# # from domain.notice import notice_router
# from domain.project import project_router
from domain.study import study_router
from domain.user import user_router

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"    # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
# app.include_router(event_router.router)
app.include_router(timeline_router.router)
# app.include_router(notice_router.router)
# app.include_router(project_router.router)
app.include_router(study_router.router)
