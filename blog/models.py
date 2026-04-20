from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.orm import Base

# Article 모델
class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(
        String(255)
    )
    content: Mapped[str] = mapped_column(
        String(1000)
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan"
    )

# Comment 모델
class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    author: Mapped[str] = mapped_column(
        String(20)
    )
    content: Mapped[str] = mapped_column(
        String(200)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    article_id: Mapped[int] = mapped_column(
        ForeignKey("article.id"),
        nullable=False
    )
    article: Mapped["Article"] = relationship(
        back_populates="comments"
    )