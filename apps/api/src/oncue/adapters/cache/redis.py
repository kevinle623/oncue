from redis.asyncio import Redis, from_url

from oncue.settings import settings

redis: Redis = from_url(settings.redis_url, decode_responses=True)
