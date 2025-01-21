from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .messages import Role
from models.historic_messages_model import MessageDB, MessageHistoryDB

def chat_history_from_id(message_history_id, session):
    stmt = select(MessageHistoryDB).where(
        MessageHistoryDB.id == message_history_id)

    try:
        chat = session.scalars(stmt).one()
    except NoResultFound:
        chat = MessageHistoryDB(id=message_history_id)

    return chat


def save_user_message_in_chat(content, chat):
    chat.messages.append(MessageDB(role=Role.human.name, content=content))


def save_assistant_message_in_chat(content, chat):
    chat.messages.append(MessageDB(role=Role.assistant.name, content=content))
