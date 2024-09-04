from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/data")
async def receive_data(data):
    # Process data here
    return {"status": "success", "data": data.dict()}
