from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import time

Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite3')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

class User_data(BaseModel):
    login: str
    password: str

class Time_data(BaseModel):
    login: str
    level: int = 0
    time0: int

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    time1 = Column(Time)
    time2 = Column(Time)
    time3 = Column(Time)
    time4 = Column(Time)
    time5 = Column(Time)
    time0 = Column(Time)

def float_to_time(santiseconds):
    if santiseconds >= 360000:
        santiseconds = 359999
    minutes, santiseconds = divmod(santiseconds, 6000)
    seconds, santiseconds = divmod(santiseconds, 100)
    return time(minute=minutes, second=seconds, microsecond=santiseconds * 10000)

def time_reformat(t: time):
    return f"{t.minute}:{t.second}:{t.microsecond // 10000}"

@app.get("/leaderboard/{level}")
async def get_leaderboard(level: int):
    query = session.query(User.login, getattr(User, f"time{level}")).all()
    result = {row.login: time_reformat(row._mapping[getattr(User, f"time{level}")]) for row in query}
    return JSONResponse(content=result, media_type="application/json")

@app.post("/register")
async def new_user(data: User_data):
    query = session.query(User).filter(User.login == data.login)
    if query.all():
        response = {"status": "error"}
    else:
        new_user = User(login=data.login, password=data.password)
        session.add(new_user)
        session.commit()
        response = {"status": "success"}  
    return JSONResponse(content=response, media_type="application/json")
    
@app.post("/login")
async def login(data: User_data):
    query = session.query(User).filter(User.login == data.login, User.password == data.password)
    if query.all():
        response = {"status": "success"}
    else:
        response = {"status": "error"}
    return JSONResponse(content=response, media_type="application/json")
    
@app.post("/insert")
async def insert_time(data: Time_data):
    query = session.query(User).filter(User.login == data.login).first()
    if query:
        setattr(query, f"time{data.level}", float_to_time(data.time0))
        session.commit()
        response = {"status": "success"}
    else:
        response = {"status": "error"}
    return JSONResponse(content=response, media_type="application/json")