from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleResponse


async def get_article_by_id(db: AsyncSession, article_id: int):
    result = await db.execute(select(Article).where(Article.id == article_id).options(selectinload(Article.author)))
    return result.scalar_one_or_none()

async def get_user_articles(db: AsyncSession, user_id: int):
    result = await db.execute(select(Article).where(Article.user_id == user_id).options(selectinload(Article.author)))
    return result.scalars().all()

async def get_articles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Article).offset(skip).limit(limit).order_by(Article.published.desc()).options(selectinload(Article.author)))
    return result.scalars().all()

async def create_article(db: AsyncSession, article_data: ArticleCreate, user_id: int):
    article = Article(
        title=article_data.title,
        content=article_data.content,
        user_id=user_id,
        rating=0
    )
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article