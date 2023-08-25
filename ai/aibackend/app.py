# ai디렉토리에서 실행하기 :  uvicorn aibackend.app:app --reload --port 5000
# 마이그레이션하기 :  alembic revision --autogenerate -m "Added some column"


from fastapi import FastAPI
from .settings import get_application
from .urls import set_routes

app = get_application()

set_routes(app)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

