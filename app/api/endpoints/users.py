from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.crud.article import get_user_articles
from app.models.user import User
from app.schemas.article import ArticleResponse
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/articles", response_model=List[ArticleResponse])
async def read_user_articles(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    from app.crud.article import get_user_articles
    from sqlalchemy import select

    # Получаем статьи пользователя
    articles = await get_user_articles(db, current_user.id)

    # Формируем ответ
    response_articles = []
    for article in articles:
        response_articles.append(
            ArticleResponse(
                id=article.id,
                title=article.title,
                content=article.content[:200] + "..." if len(article.content) > 200 else article.content,
                author=article.author.username,  # ← доступ к имени автора через отношение
                rating=article.rating,
                published=article.published,
                author_id=article.user_id  # ← user_id как author_id
            )
        )

    return response_articles

@router.put("/me", response_model=UserResponse)
async def update_user(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    pass