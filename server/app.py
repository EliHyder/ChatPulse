from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DB.db import init_db
from routers import mensages, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(user.router)
app.include_router(mensages.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the ChatPulse API!"}