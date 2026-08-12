from typing import Any

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import EntityBase


class AuditLog(EntityBase):
    __tablename__ = "audit_logs"

    actor_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[str | None] = mapped_column(String(100), index=True)
    before_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    after_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    ip_address: Mapped[str | None] = mapped_column(INET)
