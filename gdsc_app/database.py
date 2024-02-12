# 데이터베이스 설정과 연결 관리

# sqlalchemy: 데이터베이스와 상호작용하는 코드를 python 객체로 작성 가능
from sqlalchemy import create_engine # 데이터베이스와 연결 설정
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5433/db" 
# SQLALCHEMY_DATABASE_URL = "postgresql://lkpqspta:ri1wDCZRnbp-hymQBasoEycjWjPB_Mgp@arjuna.db.elephantsql.com/lkpqspta"
# postgresql://[아이디]:[비밀번호]@[db url 또는 ip]/[데이터베이스이름]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # connect_args={"check_same_thread": False} # connect_args는 SQLite에만 필요
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 데이터베이스 세션 생성

Base = declarative_base() # ORM 모델 기본 클래스 생성