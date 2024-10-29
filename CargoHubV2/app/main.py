from fastapi import FastAPI

app = FastAPI()

# routers gebruiken
app.include_router(user_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def stat():
    return {"status": "originele data hebben en controllers maken"}
