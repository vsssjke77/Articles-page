import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.database import Base



class Article(Base):
    __tablename__ = 'articles'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    rating: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    published: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )

    author: Mapped["User"] = relationship("User", back_populates="articles")


