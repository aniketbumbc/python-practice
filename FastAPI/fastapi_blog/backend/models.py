from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User (Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email:Mapped[str] = mapped_column(String(120),unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None
    )

    posts:Mapped[list[Post]] = relationship(back_populates="author")
    
    @property
    def image_path(self)->str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        
        return "/media/profile_pics/default.jpg"
    


class Post(Base):
    __tablename__ = "blogposts"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String, nullable=False)
    topic:Mapped[str] = mapped_column(String, nullable=False)
    content:Mapped[str] = mapped_column(String, nullable=False)
    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_posted:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    author: Mapped[User] = relationship(back_populates="posts")

