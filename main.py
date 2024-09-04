from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    print("Root open")
    return {"message": "Hello, World!"}

@app.post("/data")
async def receive_data(data):
    # Process data here
    print("Data post")
    return {"status": "success", "data": data.dict()}
