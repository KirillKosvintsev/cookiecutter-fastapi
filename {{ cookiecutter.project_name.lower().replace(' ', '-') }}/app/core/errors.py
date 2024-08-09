from fastapi import HTTPException, status


class PredictException(BaseException):
    ...


class ModelLoadException(BaseException):
    ...


class RepositoryError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )


class ServiceInitializationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
