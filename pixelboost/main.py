import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI

from pixelboost import config
from .api import api_router
from .models import User

app = FastAPI()

# DATABASE
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_DATABASE_URI)
    db = client.get_database(config.DATABASE_NAME)

    await init_beanie(database=db, document_models=[User])

@app.on_event("startup")
async def start_db():
    await init_db()


api = FastAPI(
    title="Pixel Boost",
    root_path="/api",
)

api.include_router(api_router)
app.mount('/api', app=api)
