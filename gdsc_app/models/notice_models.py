from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Enum, Date
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from ..database import Base

class Notice(Base):
    __tablename__ = "notice"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer) 
    tag = Column(JSON)
    upload_date = Column(Date)
    view = Column(Integer)
    photo_ids = Column(JSON)
    content = Column(String)

# 1. 제목
# 2. 작성자
# 3. 태그
# 4. 날짜
# 5. 조회수
# 6. 사진
# 7. 공지 내용