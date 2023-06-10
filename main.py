from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session
import os

from typing import Dict, Any




def create_app() -> FastAPI:

    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")

    return app, templates


def connect_db():
    global engine, metadata, SessionLocal, Base

    id = os.environ.get('ID')
    password = os.environ.get('PASSWORD')

    # 데이터베이스 설정
    DATABASE_URL = f'mysql://{id}:{password}@localhost:3306/test' 

    engine = create_engine(DATABASE_URL)
    metadata = MetaData()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app, templates = create_app()
connect_db()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tables")
def read_tables(request: Request, db: Session = Depends(get_db)):
    metadata.reflect(bind=engine)  # reflect 메소드를 이용하여 메타데이터에 테이블 정보를 로드합니다.
    tables = metadata.tables  # 메타데이터의 tables 객체를 사용하여 테이블 목록을 가져옵니다.'
    # return {"tables": [table for table in tables]}

    return templates.TemplateResponse("tableList.html", {"request": request, "tables": [table for table in tables]})




@app.get("/tables/{table_name}")
def read_table_fields(request: Request, table_name: str, db: Session = Depends(get_db)):
    metadata.reflect(bind=engine)
    table = metadata.tables.get(table_name)  # 특정 테이블 가져오기
    
    if table == None:
        return {"error": f"No table named {table_name}"}
    
    primary_keys = [key.name for key in table.primary_key]
    fields = [{"name": column.key, "type": str(column.type)} for column in table.columns]

    # return {"table": table_name, "primary_keys": primary_keys, "fields": fields}

    return templates.TemplateResponse("detailTable.html", 
            {"request": request, "table": table_name, "primary_keys": primary_keys, "fields": fields})




@app.post("/table/data")
async def create_item(item: Dict[str, int], db: Session = Depends(get_db)):
    print(item)
    metadata.reflect(bind=engine)

    for key, value in item.items():
        insert_data(key, value, db)


def insert_data(table_name: str, quantity: int, db: Session = Depends(get_db)):




    # 테이블 이름을 가지고
    table = metadata.tables.get(table_name) 

    primary_keys = [key.name for key in table.primary_key]
    fields = [{"name": column.key, "type": str(column.type)} for column in table.columns]

    Base = automap_base(metadata=metadata)
    Base.prepare()

    DynamicModel = Base.classes[table_name]


    for i in range(quantity):
        new_instance = DynamicModel()

        for field in fields:
            if field["name"] in primary_keys:
                continue

            field_type = field["type"]
            setattr(new_instance, field["name"], create_random_item(field_type))

        db.add(new_instance)
        db.commit()





import re

def create_random_item(field_type: str):
    
    for pattern, value in pattern_values.items():
        if re.match(pattern, field_type):
            return value
    return None  # 반환할 값이 없을 때는 None 반환

# 패턴-값 목록을 딕셔너리로 지정
pattern_values = {
    'INTEGER': 3,
    '^VARCHAR.*': 'Matched all alphabets',
}