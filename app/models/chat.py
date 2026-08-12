from sqlalchemy import BigInteger, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import EntityBase


class ChatRoom(EntityBase):
    __tablename__ = "chat_rooms"

    survey_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    access_type: Mapped[str] = mapped_column(String(20), nullable=False, default="survey")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)

    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="room")


class ChatMessage(EntityBase):
    __tablename__ = "chat_messages"
    __table_args__ = (
        UniqueConstraint("room_id", "msg_seq"),
        Index("ix_chat_messages_room_created", "room_id", "created_at"),
    )

    room_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False
    )
    sender_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    msg_seq: Mapped[int] = mapped_column(BigInteger, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False, default="text")
    content: Mapped[str] = mapped_column(Text, nullable=False)

    room: Mapped[ChatRoom] = relationship(back_populates="messages")
