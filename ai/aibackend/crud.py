from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import *  # 모델의 위치에 따라 경로를 적절히 수정해주세요

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Crud:
    def __init__(self, table):
        self.table = table

    def create_item(self, item, db: Session):
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def read_item(self, item_id: int, db: Session):
        item = db.query(self.table).filter(self.table.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def update_item(self, item_id: int, item, db: Session):
        db_item = db.query(self.table).filter(self.table.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        for key, value in item.dict().items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item

    def delete_item(self, item_id: int, db: Session):
        db_item = db.query(self.table).filter(self.table.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        db.delete(db_item)
        db.commit()
        return db_item
