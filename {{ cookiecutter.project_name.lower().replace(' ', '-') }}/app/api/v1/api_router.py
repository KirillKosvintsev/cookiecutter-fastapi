from fastapi import APIRouter

from app.api.v1.example_router import example_router


api_router = APIRouter(prefix="/v1")
api_router.include_router(example_router, tags=["example"])

# Add more routers to /v1 here:
# api_router.include_router(users_router, tags=["users"])
# api_router.include_router(items_router, tags=["items"])
