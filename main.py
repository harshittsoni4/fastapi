from fastapi import Depends, FastAPI ,HTTPException , Response
from random import randint
from datetime import datetime,timezone
from typing import Annotated, Any
from fastapi.concurrency import asynccontextmanager
from sqlmodel import Field, create_engine,SQLModel,Session, select

class Campaign(SQLModel,table=True):
    campaign_id:int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime |None = Field(default=None,index=True)
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc),nullable=True,index=True)

sqlite_file_name="database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args={"check_same_thread":False}
engine =create_engine(sqlite_url,connect_args=connect_args)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]    

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="hArshit",due_date=datetime.now()),
                Campaign(name="vaibhavi",due_date=datetime.now())
            ])
            session.commit()
    yield

app =FastAPI(root_path="/api/v1",lifespan=lifespan)
# fastapi dev main.py
# app = FastAPI(root_path="/api/v1")
@app.get("/") #main route
async def root():
    return {"message": "Hello"}

data : Any =[{
    "campaign_id":1,
    "name":"capmaign  summar",
    "due date": datetime.now(),
    "created_at":datetime.now()
},{
    "campaign_id":2,
        "name":"capmaign winter",
        "due date": datetime.now(),
        "created_at":datetime.now()
},{
    "campaign_id":3,
        "name":"capmaign  autumn",
        "due date": datetime.now(),
        "created_at":datetime.now()
}]
@app.get("/campaigns") #getting all data
async def read_capmpaigns(session:SessionDep):
    data=session.exec(select(Campaign)).all()
    return {"campaign":data}

# @app.get("/campaigns") #getting all data
# async def read_capmpaigns():
#     return {"campaign":data}
# @app.get("/campaigns/{id}") #getting data by id
# async def read_camp(id:int):
#     for campaign in data:
#         if campaign.get("campaign_id")== id : 
#             return {"campaign": campaign}
#     raise HTTPException(status_code=404) 

# @app.post("/campaigns",status_code=201) #creating new data
# async def create_campaign(id:int,body:dict[str,Any]):
#     # body = await request.json()
#     new :Any ={
#          "campaign_id":randint(1,1000),
#                 "name":body.get("name"),
#                 "due date": body.get("due_date"),
#                 "created_at":datetime.now()
#     }
#     data.append(new)
#     return {"campaign":new}

# @app.put("/campaigns/{id}",) #updating data by id
# async def update_campaign(id:int, body: dict[str,Any]):
#     for index,campaign in enumerate(data):
#         if campaign.get("campaign_id")==id:

#             updated :Any ={
#                 "campaign_id":id,
#                                 "name":body.get("name"),
#                                 "due date": body.get("due_date"),
#                                 "created_at":campaign.get("created_at")
#             }
#             data[index]=updated
#             return {"campaign":updated}
#     raise HTTPException(status_code=404)


# @app.delete("/campaigns/{id}",) #deleting data by id
# async def delete_campaign(id:int):
#     for index,campaign in enumerate(data):
#         if campaign.get("campaign_id")==id:
#             data.pop(index)
#             return Response(status_code=204)
#     raise HTTPException(status_code=404)
