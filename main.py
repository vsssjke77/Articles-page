from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.endpoints import auth, users, articles
from app.database.database import async_engine, Base
from app.database.redis_client import redis_client
from config import settings

app = FastAPI(
    title="Article Website API",
    description="API для сайта со статьями с кэшированием в Redis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация роутеров
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])


@app.on_event("startup")
async def startup():
    print("🚀 Starting application...")

    try:
        # Создаем таблицы (если их нет)
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Database tables ready")

    except Exception as e:
        print(f"❌ Database error: {e}")
        print("⚠️ Starting without database...")

    # Redis
    try:
        await redis_client.connect()
        print("✅ Redis connected")
    except Exception as e:
        print(f"❌ Redis error: {e}")

    print("🎯 Application started successfully!")

@app.on_event("shutdown")
async def shutdown():
    await redis_client.disconnect()

@app.get("/")
async def root():
    return {"message": "Article Website API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}