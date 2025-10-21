import redis.asyncio as redis
from config import settings


class RedisClient:
    def __init__(self):
        self.redis = None

    async def connect(self):
        print("🔌 Подключаемся к Redis...")
        self.redis = redis.from_url(settings.redis_url)
        await self.redis.ping()
        print("✅ Redis подключен!")

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            print("🔌 Redis отключен")

    async def get_article_content(self, article_id: int):
        if not self.redis:
            return None
        key = f"article:{article_id}:content"
        print(f"🔍 Redis: Получаем ключ {key}")
        return await self.redis.get(key)

    async def set_article_content(self, article_id: int, content: str, expire: int = 20):
        if not self.redis:
            return
        key = f"article:{article_id}:content"
        print(f"💾 Redis: Устанавливаем ключ {key} на {expire} секунд")
        await self.redis.setex(key, expire, content)


redis_client = RedisClient()