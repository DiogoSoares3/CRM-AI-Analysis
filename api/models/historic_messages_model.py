from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from chat.messages import Message, MessageHistory, Role


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models, defining default table configurations.

    Attributes:
        __table_args__ (dict):
            Specifies the default schema ('public') for all tables.
    """
    __table_args__ = {'schema': 'public'}
    pass


class MessageHistoryDB(Base):
    """
    Represents a chat history stored in the database.

    Attributes:
        __tablename__ (str): 
            The name of the database table ("message_history").
        id (int): 
            The primary key identifier for the chat history.
        messages (List[MessageDB]): 
            A list of messages related to this chat history.

    Methods:
        to_message_history() -> MessageHistory:
            Converts the database object into a `MessageHistory` instance.
        to_list() -> list:
            Converts the stored messages into a list of dictionaries.
    """

    __tablename__ = "message_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[List["MessageDB"]] = relationship(
        back_populates="message_history",
        cascade="all, delete-orphan"
    )

    def to_message_history(self) -> MessageHistory:
        """
        Converts the stored messages into a `MessageHistory` object.

        Returns:
            MessageHistory:
                A `MessageHistory` instance containing all messages.
        """
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
        """
        Converts the stored messages into a list of dictionaries.

        Returns:
            list:
                A list containing message dictionaries with `role` and `content`.
        """
        msg_list = []
        for msg in self.messages:
            msg_list.append(msg.to_dict())

        return msg_list


class MessageDB(Base):
    """
    Represents an individual chat message stored in the database.

    Attributes:
        __tablename__ (str): 
            The name of the database table ("message").
        id (int): 
            The primary key identifier for the message.
        role (str): 
            The role of the sender (e.g., "human", "assistant", "system").
        content (str): 
            The actual message content.
        message_history_id (int): 
            The foreign key linking this message to a chat history.
        message_history (MessageHistoryDB): 
            The associated chat history.

    Methods:
        to_dict() -> dict:
            Converts the message into a dictionary format.
    """

    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(String(2000))
    message_history_id: Mapped[int] = mapped_column(
        ForeignKey("public.message_history.id"))
    message_history: Mapped["MessageHistoryDB"] = relationship(
        back_populates="messages")

    def to_dict(self) -> dict:
        """
        Converts the message into a dictionary format.

        Returns:
            dict:
                A dictionary containing the `role` and `content` of the message.
        """
        return {'role': self.role, 'content': self.content}
