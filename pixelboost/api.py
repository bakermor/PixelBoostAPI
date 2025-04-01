from fastapi import APIRouter

from .auth.views import router as user_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users")

@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
