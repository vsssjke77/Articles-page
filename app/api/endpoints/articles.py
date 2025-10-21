from typing import List

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.crud.article import create_article, get_article_by_id, get_articles
from app.database.database import async_session_factory
from app.models.article import Article
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleResponse
from app.services.cache_service import cache_service

router = APIRouter()

@router.post("/", response_model=ArticleResponse)
async def create_new_article(
        article_data: ArticleCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    article = await create_article(db, article_data, current_user.id)

    response_data = ArticleResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        author=current_user.username,
        rating=article.rating,
        published=article.published,
        author_id=article.user_id
    )

    return response_data

@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article_by_his_id(article_id: int, db: AsyncSession = Depends(get_db)):
    article = await get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    content = await cache_service.get_article_with_cache(article_id, db)

    response_data = ArticleResponse(
        id=article.id,
        title=article.title,
        content=content,
        author=article.author.username,
        rating=article.rating,
        published=article.published,
        author_id=article.user_id
    )
    return response_data

@router.get("/", response_model=List[ArticleResponse])
async def get_all_articles(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    articles = await get_articles(db, skip=skip, limit=limit)
    response_articles = []
    if articles:
        for article in articles:
            content = await cache_service.get_article_with_cache(article.id, db)
            response_articles.append(
                ArticleResponse(
                    id=article.id,
                    title=article.title,
                    content=content[:200] + "..." if len(content) > 200 else content,  # Preview
                    author=article.author.username,
                    rating=article.rating,
                    published=article.published,
                    author_id=article.user_id
                )
            )

    return response_articles

@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article():
    pass