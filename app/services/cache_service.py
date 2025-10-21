from app.database.redis_client import redis_client
from app.crud.article import get_article_by_id


class CacheService:
    @staticmethod
    async def get_article_with_cache(article_id: int, db):
        print(f"🔍 CacheService: Получение статьи {article_id}")

        # Пытаемся получить из кэша
        cached_content = await redis_client.get_article_content(article_id)
        if cached_content:
            print(f"✅ Статья {article_id} найдена в кэше")
            return cached_content.decode('utf-8')

        print(f"❌ Статья {article_id} не в кэше, получаем из БД")

        # Если нет в кэше, получаем из БД и кэшируем
        article = await get_article_by_id(db, article_id)
        if article:
            print(f"💾 Кэшируем статью {article_id} на 20 секунд")
            await redis_client.set_article_content(article_id, article.content)
            return article.content

        print(f"❌ Статья {article_id} не найдена в БД")
        return None


cache_service = CacheService()