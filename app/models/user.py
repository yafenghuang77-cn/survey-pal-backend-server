from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, EntityBase, IdMixin, TimestampMixin


class User(EntityBase):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            "uq_users_phone_active",
            "phone",
            unique=True,
            postgresql_where=text("NOT is_deleted"),
        ),
        Index(
            "uq_users_email_active",
            "email",
            unique=True,
            postgresql_where=text("NOT is_deleted"),
        ),
    )

    phone: Mapped[str | None] = mapped_column(String(32))
    email: Mapped[str | None] = mapped_column(String(320))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    nickname: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)

    sessions: Mapped[list["UserSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserSession(Base, IdMixin, TimestampMixin):
    __tablename__ = "user_sessions"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    device_info: Mapped[str | None] = mapped_column(String(255))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="sessions")
