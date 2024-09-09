from fastapi import FastAPI
from fastapi.responses import Response
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
    time_new: int

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
    centies = t.microsecond // 10000
    return f"{t.minute:02}:{t.second:02}:{centies:02}"

@app.get("/test")
async def test_reader():
    return {"status": "success"}
    
@app.get("/leaderboard/{level}")
async def get_leaderboard(level: int):
    query = session.query(User.login, getattr(User, f"time{level}")).all()
    if query:
        dictionary = {row.login: time_reformat(row._mapping[getattr(User, f"time{level}")]) for row in query}
        result = dict(sorted(dictionary.items(), key=lambda x: x[1]))
        for key in result:
            print(key, result[key])
        return {"status": "success", "data": result}
    else:
        return {"status": "error"}

@app.post("/register")
async def new_user(data: User_data):
    query = session.query(User).filter(User.login == data.login)
    if query.all():
        return {"status": "error"}
    else:
        new_user = User(login=data.login, password=data.password)
        session.add(new_user)
        session.commit()
        return {"status": "success"} 
    
@app.post("/login")
async def login(data: User_data):
    query = session.query(User).filter(User.login == data.login, User.password == data.password)
    if query.all():
        return {"status": "success"}
    else:
        return {"status": "error"}
    
@app.post("/insert/{level}")
async def insert_time(data: Time_data, level: int):
    query = session.query(User).filter(User.login == data.login).first()
    if query:
        new_time = float_to_time(data.time_new)
        if getattr(query, f"time{level}") == None or new_time < getattr(query, f"time{level}"):
            setattr(query, f"time{level}", new_time)
        session.commit()
        return {"status": "success"}
    else:
        return {"status": "error"}