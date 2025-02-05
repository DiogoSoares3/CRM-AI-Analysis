from fastapi import APIRouter, Depends

from models.historic_messages_model import Message
from core.database import engine
from core.deps import get_session
from core.configs import settings
from chat.services import chat_history_from_id


router = APIRouter(tags=['Chat'])


@router.post(
    "/historic-message/",
    status_code=200,
    description="Return historic messages from the chat"
)
async def historic_message(
    message: Message,
    session=Depends(get_session)
):
    """
    Retrieves historical messages from a chat session.

    Args:
        message (Message):
            The message object containing the chat history ID.
        session (Session):
            The database session dependency.

    Returns:
        chat (list):
            A list of messages from the chat history.
    """
    with session:
        chat = chat_history_from_id(
            message_history_id=message.message_history_id,
            session=session
        ).to_list()
        
        session.commit()

    return chat
