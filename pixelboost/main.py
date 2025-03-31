from fastapi import FastAPI
import motor.motor_asyncio
from beanie import init_beanie
from .models import BaseUser
from .enums import CollectionNames
from .api import api_router
from pixelboost import config

app = FastAPI()

# DATABASE
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_DATABASE_URI)
    db = client.get_database(config.DATABASE_NAME)

    await init_beanie(database=db, document_models=[BaseUser])

@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router)
