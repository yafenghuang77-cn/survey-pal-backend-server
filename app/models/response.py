from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import EntityBase


class Response(EntityBase):
    __tablename__ = "responses"
    __table_args__ = (
        UniqueConstraint("survey_version_id", "idempotency_key"),
        Index("ix_responses_version_submitted", "survey_version_id", "submitted_at"),
    )

    survey_version_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("survey_versions.id", ondelete="RESTRICT"), nullable=False
    )
    respondent_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    answers: Mapped[list["ResponseAnswer"]] = relationship(
        back_populates="response", cascade="all, delete-orphan"
    )


class ResponseAnswer(EntityBase):
    __tablename__ = "response_answers"
    __table_args__ = (UniqueConstraint("response_id", "question_id"),)

    response_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("responses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False
    )
    answer: Mapped[dict[str, Any] | list[Any] | str | int | float | bool | None] = mapped_column(
        JSONB, nullable=True
    )

    response: Mapped[Response] = relationship(back_populates="answers")
