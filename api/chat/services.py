from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .messages import Role
from models.historic_messages_model import MessageDB, MessageHistoryDB

def chat_history_from_id(message_history_id: str, session) -> MessageHistoryDB:
    """
    Retrieves a chat history from the database based on the given ID.

    Args:
        message_history_id (str):
            The unique identifier of the chat history.
        session (Session):
            The database session used to execute the query.

    Returns:
        MessageHistoryDB:
            The retrieved chat history object. If not found, a new instance is created.

    Raises:
        NoResultFound:
            If no chat history is found, a new one is instantiated instead.
    """
    stmt = select(MessageHistoryDB).where(
        MessageHistoryDB.id == message_history_id
    )

    try:
        chat = session.scalars(stmt).one()
    except NoResultFound:
        chat = MessageHistoryDB(id=message_history_id)

    return chat


def save_user_message_in_chat(content: str, chat: MessageHistoryDB) -> None:
    """
    Saves a user message in the chat history.

    Args:
        content (str):
            The message content from the user.
        chat (MessageHistoryDB):
            The chat history object where the message should be stored.
    """
    chat.messages.append(MessageDB(role=Role.human.name, content=content))


def save_assistant_message_in_chat(content: str, chat: MessageHistoryDB) -> None:
    """
    Saves an assistant message in the chat history.

    Args:
        content (str):
            The message content from the assistant.
        chat (MessageHistoryDB):
            The chat history object where the message should be stored.
    """
    chat.messages.append(MessageDB(role=Role.assistant.name, content=content))