from fastapi import APIRouter, HTTPException

from app.schemas.schemas import HealthResponse


system_router = APIRouter(prefix='', tags=["system"])


@system_router.get(
    "/healthz",
    response_model=HealthResponse,
)
async def healthz():
    is_health = False
    try:
        # add your logic here
        is_health = True
        return HealthResponse(status=is_health)
    except Exception:
        raise HTTPException(status_code=404, detail="Unhealthy")


@system_router.get(
    "/readyz",
    response_model=HealthResponse,
)
async def readyz():
    is_ready = False
    try:
        # add your logic here

        # from services.predict import MachineLearningModelInference as model
        # test_input = MachineLearningDataInput(
        #     **json.loads(open(settings.model.input_example, "r").read())
        # )
        # test_point = test_input.get_np_array()
        # model.predict(data_point, load_wrapper=joblib.load, method="predict")
        is_ready = True
        return HealthResponse(status=is_ready)
    except Exception:
        raise HTTPException(status_code=404, detail="Unready")
