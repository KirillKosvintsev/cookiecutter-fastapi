from aiocache import Cache
from aiocache.serializers import PickleSerializer
from functools import wraps
from config.config import settings


cache = Cache(Cache.MEMORY)


# Функция для создания кэша в зависимости от настроек
async def setup_cache():
    global cache
    if settings.cache.backend == "redis":
        from aiocache import RedisCache
        cache = RedisCache(
            endpoint=settings.cache.redis_host,
            port=settings.cache.redis_port,
            namespace=settings.cache.namespace,
            serializer=PickleSerializer()
        )
    elif settings.cache.backend == "memcached":
        from aiocache import MemcachedCache
        cache = MemcachedCache(
            endpoint=settings.cache.memcached_host,
            port=settings.cache.memcached_port,
            namespace=settings.cache.namespace,
            serializer=PickleSerializer()
        )
    else:
        # По умолчанию используем in-memory кэш
        cache = Cache(Cache.MEMORY, namespace=settings.cache.namespace)


# Декоратор для кэширования результатов функций
def cached(ttl=300, key_builder=None):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            key = key_builder(*args, **kwargs) if key_builder else Cache.KEY_BUILDER(*args, **kwargs)
            result = await cache.get(key)
            if result is None:
                result = await func(*args, **kwargs)
                await cache.set(key, result, ttl=ttl)
            return result
        return wrapped
    return wrapper


# Функция для очистки кэша
async def clear_cache():
    await cache.clear()


# Функция для получения значения из кэша
async def get_cached(key):
    return await cache.get(key)


# Функция для установки значения в кэш
async def set_cached(key, value, ttl=None):
    await cache.set(key, value, ttl=ttl)


# Функция для удаления значения из кэша
async def delete_cached(key):
    await cache.delete(key)


# Функция для получения статистики кэша
async def get_cache_stats():
    return await cache.get_stats()
