from fastapi import FastAPI

app = FastAPI()

@app.post("/data")
async def receive_data(data):
    # Process data here
    return {"status": "success", "data": data.dict()}
