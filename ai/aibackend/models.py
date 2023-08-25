# makemigrations :  alembic revision --autogenerate -m "Added some column"
# migrate :  alembic upgrade head




from sqlalchemy import Column, Integer, String, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import *

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Chatbot(Base):
    __tablename__ = 'chatbot'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50)) 
    query = Column(Text)
    intent = Column(String(50))
    ner = Column(String(200))

    

# 데이터베이스 연결
DATABASE_URL = f"mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"

engine = create_engine(DATABASE_URL)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
