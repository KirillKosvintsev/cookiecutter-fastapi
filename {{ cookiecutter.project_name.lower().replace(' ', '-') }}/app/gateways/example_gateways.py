from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Type
import aiohttp
import requests
from pydantic import BaseModel


class RequestError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(
            f"Request failed with status {status_code}: {message}")


class BaseGateway(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    async def request(self, method: str, endpoint: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def handle_response(self, response: Any) -> Any:
        pass

    @abstractmethod
    def handle_error(self, error: Any) -> None:
        pass


class AsyncGateway(BaseGateway):
    async def request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                try:
                    return await self.handle_response(response)
                except Exception as e:
                    self.handle_error(e)

    async def handle_response(self, response: aiohttp.ClientResponse) -> Any:
        if response.status >= 400:
            raise RequestError(response.status, await response.text())
        return await response.json()

    def handle_error(self, error: Exception) -> None:
        # Log the error or perform any other error handling
        raise error


class SyncGateway(BaseGateway):
    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        try:
            return self.handle_response(response)
        except Exception as e:
            self.handle_error(e)

    def handle_response(self, response: requests.Response) -> Any:
        response.raise_for_status()
        return response.json()

    def handle_error(self, error: Exception) -> None:
        # Log the error or perform any other error handling
        raise error


class PaginatedGateway(AsyncGateway):
    async def paginated_request(self, method: str, endpoint: str,
                                page_param: str = "page",
                                limit_param: str = "limit", **kwargs) -> List[
        Dict]:
        all_results = []
        page = 1
        while True:
            params = kwargs.get("params", {})
            params.update({page_param: page, limit_param: 100})
            kwargs["params"] = params

            results = await self.request(method, endpoint, **kwargs)
            if not results:
                break

            all_results.extend(results)
            page += 1

        return all_results


class ModelGateway(AsyncGateway):
    def __init__(self, base_url: str, model: Type[BaseModel]):
        super().__init__(base_url)
        self.model = model

    async def handle_response(self, response: aiohttp.ClientResponse) -> Union[
        BaseModel, List[BaseModel]]:
        if response.status >= 400:
            raise RequestError(response.status, await response.text())

        data = await response.json()
        if isinstance(data, list):
            return [self.model(**item) for item in data]
        return self.model(**data)


class CachedGateway(AsyncGateway):
    def __init__(self, base_url: str, cache_backend: Any):
        super().__init__(base_url)
        self.cache = cache_backend

    async def request(self, method: str, endpoint: str, use_cache: bool = True,
                      cache_ttl: int = 3600, **kwargs) -> Any:
        if use_cache and method.lower() == "get":
            cache_key = f"{method}:{endpoint}:{kwargs}"
            cached_response = await self.cache.get(cache_key)
            if cached_response:
                return cached_response

        response = await super().request(method, endpoint, **kwargs)

        if use_cache and method.lower() == "get":
            await self.cache.set(cache_key, response, expire=cache_ttl)
        return response
