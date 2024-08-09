import os

from loguru import logger

from core.errors import PredictException, ModelLoadException
from config.config import settings


class MachineLearningModelHandlerScore(object):
    model = None

    @classmethod
    def predict(cls, input, load_wrapper=None, method="predict"):
        clf = cls.get_model(load_wrapper)
        if hasattr(clf, method):
            return getattr(clf, method)(input)
        raise PredictException(f"'{method}' attribute is missing")

    @classmethod
    def get_model(cls, load_wrapper):
        if cls.model is None and load_wrapper:
            cls.model = cls.load(load_wrapper)
        return cls.model

    @staticmethod
    def load(load_wrapper):
        model = None
        model_path = settings.model.model_path
        model_name = settings.model.model_name
        if settings.model.model_path.endswith("/"):
            path = f"{model_path}{model_name}"
        else:
            path = f"{model_path}/{model_name}"
        if not os.path.exists(path):
            message = f"Machine learning model at {path} not exists!"
            logger.error(message)
            raise FileNotFoundError(message)
        model = load_wrapper(path)
        if not model:
            message = f"Model {model} could not load!"
            logger.error(message)
            raise ModelLoadException(message)
        return model
