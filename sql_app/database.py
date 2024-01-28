from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://dyk6208:1234@localhost/db" 
SQLALCHEMY_DATABASE_URL = "postgresql://lkpqspta:ri1wDCZRnbp-hymQBasoEycjWjPB_Mgp@arjuna.db.elephantsql.com/lkpqspta"
# postgresql://[아이디]:[비밀번호]@[db url 또는 ip]/[데이터베이스이름]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # connect_args={"check_same_thread": False} # connect_args는 SQLite에만 필요
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()