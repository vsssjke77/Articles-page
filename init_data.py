import asyncio
import aiohttp
import random
from faker import Faker
import json

fake = Faker()

API_BASE_URL = "http://localhost:8000"


async def register_user(session, username, email, password):
    """Регистрация пользователя через API"""
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        async with session.post(f"{API_BASE_URL}/auth/register", json=user_data) as response:
            if response.status == 200:
                user = await response.json()
                print(f"✅ Зарегистрирован пользователь: {user['username']}")
                return user
            else:
                error = await response.text()
                print(f"❌ Ошибка регистрации {username}: {error}")
                return None
    except Exception as e:
        print(f"❌ Ошибка подключения для {username}: {e}")
        return None


async def login_user(session, username, password):
    """Логин пользователя через API"""
    form_data = {
        "username": username,
        "password": password
    }

    try:
        async with session.post(f"{API_BASE_URL}/auth/login", data=form_data) as response:
            if response.status == 200:
                tokens = await response.json()
                return tokens["access_token"]
            else:
                print(f"❌ Ошибка логина {username}")
                return None
    except Exception as e:
        print(f"❌ Ошибка логина для {username}: {e}")
        return None


async def create_article(session, token, title, content):
    """Создание статьи через API"""
    article_data = {
        "title": title,
        "content": content
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with session.post(f"{API_BASE_URL}/articles/", json=article_data, headers=headers) as response:
            if response.status == 200:
                article = await response.json()
                return article
            else:
                error = await response.text()
                print(f"❌ Ошибка создания статьи: {error}")
                return None
    except Exception as e:
        print(f"❌ Ошибка создания статьи: {e}")
        return None


async def init_test_data():
    """Инициализация тестовых данных через API"""
    print("🚀 Начинаем инициализацию тестовых данных через API...")

    async with aiohttp.ClientSession() as session:
        users = []

        # Создаем 20 пользователей
        print("🔄 Регистрируем пользователей...")
        for i in range(20):
            username = f"user_{i}_{fake.user_name()}"
            email = f"user_{i}_{fake.email()}"
            password = "password123"

            user = await register_user(session, username, email, password)
            if user:
                users.append({
                    "id": user["id"],
                    "username": username,
                    "password": password
                })

        print(f"✅ Зарегистрировано {len(users)} пользователей")

        # Создаем статьи для каждого пользователя
        print("🔄 Создаем статьи...")
        total_articles = 0

        for user in users:
            # Логинимся как пользователь
            token = await login_user(session, user["username"], user["password"])

            if token:
                articles_created = 0
                for j in range(50):  # По 50 статей на пользователя
                    title = fake.sentence()
                    content = fake.text(1000)  # Длинный текст

                    article = await create_article(session, token, title, content)
                    if article:
                        articles_created += 1
                        total_articles += 1

                print(f"📝 Пользователь {user['username']} создал {articles_created} статей")
            else:
                print(f"❌ Не удалось войти как {user['username']}")

        print(f"🎉 Инициализация завершена!")
        print(f"📊 Итог: {len(users)} пользователей, {total_articles} статей")




async def main():
    """Основная функция"""
    print("🔍 Проверяем существующие данные...")

    await init_test_data()


if __name__ == "__main__":
    asyncio.run(main())