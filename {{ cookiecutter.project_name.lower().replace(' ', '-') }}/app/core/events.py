from typing import Callable

import joblib
from loguru import logger
from fastapi import FastAPI

from config.config import settings


def preload_model():
    """
    SINGLETON
    """
    from services.predict import MachineLearningModelHandlerScore
    MachineLearningModelHandlerScore.get_model()


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        preload_model()
    return start_app


ml_model = None  # GLOBAL VARIABLE


async def create_start_app_handler():
    async def start_app() -> None:
        await load_ml_model()
    return start_app


async def create_stop_app_handler():
    async def stop_app() -> None:
        global ml_model
        ml_model = None
        logger.info("ML model unloaded and application shutting down")

    return stop_app


async def load_ml_model():
    global ml_model
    try:
        ml_model = joblib.load(settings.model.ML_MODEL_PATH)
    except Exception as e:
        logger.error(f"Error loading ML model: {str(e)}")
        raise


def get_ml_model():
    return ml_model
