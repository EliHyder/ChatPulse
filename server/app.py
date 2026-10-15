from fastapi import FastAPI
from DB.db import init_db
from routers import mensages, users

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(users.router)
app.include_router(mensages.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the ChatPulse API!"}