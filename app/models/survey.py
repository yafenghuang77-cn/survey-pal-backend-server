from typing import Any

from sqlalchemy import BigInteger, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import EntityBase


class Survey(EntityBase):
    __tablename__ = "surveys"

    owner_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft", index=True)
    current_version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    versions: Mapped[list["SurveyVersion"]] = relationship(
        back_populates="survey", cascade="all, delete-orphan"
    )


class SurveyVersion(EntityBase):
    __tablename__ = "survey_versions"
    __table_args__ = (UniqueConstraint("survey_id", "version"),)

    survey_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    settings: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    survey: Mapped[Survey] = relationship(back_populates="versions")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="survey_version", cascade="all, delete-orphan"
    )


class Question(EntityBase):
    __tablename__ = "questions"
    __table_args__ = (Index("ix_questions_version_position", "survey_version_id", "position"),)

    survey_version_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("survey_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_required: Mapped[bool] = mapped_column(nullable=False, default=False)
    config: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    survey_version: Mapped[SurveyVersion] = relationship(back_populates="questions")
    options: Mapped[list["QuestionOption"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )


class QuestionOption(EntityBase):
    __tablename__ = "question_options"
    __table_args__ = (
        UniqueConstraint("question_id", "value"),
        Index("ix_question_options_question_position", "question_id", "position"),
    )

    question_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(500), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    question: Mapped[Question] = relationship(back_populates="options")
