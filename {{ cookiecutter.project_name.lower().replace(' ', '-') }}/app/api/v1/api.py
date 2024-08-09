from fastapi import APIRouter

from api.v1.router_1 import router as predictor

router = APIRouter(prefix="/v1")
router.include_router(predictor.router, tags=["predictor"])
