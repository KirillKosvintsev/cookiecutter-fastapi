import joblib
from fastapi import APIRouter, HTTPException

from services.predict import MachineLearningModelInference as model
from schemas.schemas import (
    MachineLearningResponse,
    MachineLearningDataInput,
)

example_router = APIRouter()


@example_router.post(
    "/predict",
    response_model=MachineLearningResponse,
)
async def predict(data_input: MachineLearningDataInput):
    if not data_input:
        raise HTTPException(status_code=404,
                            detail="'data_input' argument invalid!")
    try:
        data_point = data_input.get_np_array()
        prediction = model.predict(data_point, load_wrapper=joblib.load,
                                   method="predict")

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Exception: {err}")

    return MachineLearningResponse(prediction=prediction)
