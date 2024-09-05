from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

class User_data(BaseModel):
    login: str
    password: str

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
    timet = Column(Time)

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