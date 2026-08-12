from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import EntityBase


class OutboxEvent(EntityBase):
    __tablename__ = "outbox_events"
    __table_args__ = (Index("ix_outbox_unpublished", "published_at", "occurred_at"),)

    event_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), default=uuid4, unique=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    aggregate_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
