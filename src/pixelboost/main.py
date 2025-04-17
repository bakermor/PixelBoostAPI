import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .api import api_router
from .models import User, Activity

app = FastAPI()

# DATABASE
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_DATABASE_URI)
    db = client.get_database(config.DATABASE_NAME)

    await init_beanie(database=db, document_models=[User, Activity])

@app.on_event("startup")
async def start_db():
    await init_db()


api = FastAPI(
    title="Pixel Boost",
    root_path="/api",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(api_router)
app.mount('/api', app=api)
