from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, db: SessionLocal = Depends(get_db)):
    db_user = User(name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: SessionLocal = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()