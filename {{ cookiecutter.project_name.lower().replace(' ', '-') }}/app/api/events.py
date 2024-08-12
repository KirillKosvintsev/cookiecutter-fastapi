from contextlib import asynccontextmanager

import joblib
from loguru import logger
from fastapi import FastAPI

from app.config.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before the app starts == @on_startup
    logger.info("Application starting")
    load_model()
    yield
    unload_model()
    # After the app stops == @on_shutdown


# Singleton pattern------------------------------------------------------------
def load_model():
    from services.predict import MachineLearningModelInference
    MachineLearningModelInference.load(joblib.load)


def unload_model():
    from services.predict import MachineLearningModelInference
    MachineLearningModelInference.model = None


# Global variable--------------------------------------------------------------
ml_model = None  # GLOBAL VARIABLE


def get_ml_model():
    return ml_model


def load_ml_model() -> None:
    global ml_model
    try:
        ml_model = joblib.load(settings.model.model_path)
    except Exception as e:
        logger.error(f"Error loading ML model: {str(e)}")
        raise


def unload_ml_model() -> None:
    global ml_model
    ml_model = None
    logger.info("ML model unloaded and application shutting down")
