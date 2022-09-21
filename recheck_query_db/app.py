from typing import Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


# TODO rework how table is called
class Table(SQLModel, table=True):
    id: int = Field(primary_key=True)
    base_url: Optional[str] = None
    status: str
    source_id: int


# supports any type of sql database example is for mysql
# db = "mysql+pymysql://user:pw@host/db"
mysql_db = "mysql+mysqlconnector://root:example@mysql/database"
engine = create_engine(mysql_db, pool_pre_ping=True)
SQLModel.metadata.create_all(engine)


# base_url: str, status: str, source_id: int

# TODO current returing an empty list?
@app.get("/")
def query_db():
    with Session(engine) as session:
        domains = session.exec(select(Table)).all()
        payload = {}
        for domain in domains:
            print(domain)
            # if domain[1] != "active" or domain[2] != 1:
            #     pass
            # else:
            #     site = domain[0]
            #     print(site, flush=True)
            #     payload.append({
            #         'domain': site
            #         })
            #     print(domains, flush=True)
        # json_ify = jsonable_encoder(payload)
        return JSONResponse(content=domains)
