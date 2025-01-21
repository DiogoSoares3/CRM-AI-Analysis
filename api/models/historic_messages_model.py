from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from chat.messages import Message, MessageHistory, Role


class Base(DeclarativeBase):
    __table_args__ = {'schema': 'public'}
    pass


class MessageHistoryDB(Base):
    __tablename__ = "message_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[List["MessageDB"]] = relationship(
        back_populates="message_history",
        cascade="all, delete-orphan"
    )

    def to_message_history(self) -> MessageHistory:
        message_history = MessageHistory()
        for msg in self.messages:
            message_history.add_message(
                Message(
                    role=Role.get(msg.role),
                    content=msg.content
                )
            )
        return message_history

    def to_list(self) -> list:
        msg_list = []
        for msg in self.messages:
            msg_list.append(msg.to_dict())

        return msg_list


class MessageDB(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(String(2000))
    message_history_id: Mapped[int] = mapped_column(
        ForeignKey("public.message_history.id"))
    message_history: Mapped["MessageHistoryDB"] = relationship(
        back_populates="messages")

    def to_dict(self):
        return {'role': self.role, 'content': self.content}
