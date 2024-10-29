from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def stat():
    return {"status": "originele data hebben en controllers maken"}
