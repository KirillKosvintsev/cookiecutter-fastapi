from fastapi import FastAPI

from app.api.v1.api_router import api_router
from app.api.system import system_router
from app.api.events import lifespan
from app.api.middleware import setup_middleware
from app.config.config import settings
from app.core.logger import setup_logging


def get_application() -> FastAPI:
    application = FastAPI(title=settings.api.title, debug=settings.debug,
                          version=settings.api.version, lifespan=lifespan)
    setup_middleware(application)
    application.include_router(system_router)
    application.include_router(api_router, prefix=settings.api.prefix)
    return application


setup_logging()

app = get_application()
