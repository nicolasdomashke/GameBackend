from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get("/")
async def read_root():
    print("Root open")
    return {"message": "Hello, World!"}

@app.post("/data")
async def receive_data(data: Item):
    # Process data here
    print("Data post")
    return {"status": "success", "data": data}
