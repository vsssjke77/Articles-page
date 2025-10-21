import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

from app.models.article import Article

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )

    articles: Mapped[list["Article"]] = relationship(
        "Article",
    back_populates="author")

