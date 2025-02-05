from pydantic import BaseModel
from typing import Literal

class SQLInjectionStatus(BaseModel):
    """
    Represents the security status of an SQL query regarding SQL injection threats.

    Attributes:
        status (Literal["Insecure", "Secure"]): 
            A status indicating whether the SQL query is "Secure" or "Insecure".
    """
    status: Literal["Insecure", "Secure"]

class SerializableChatSchema(BaseModel):
    """
    Represents a serializable chat message.

    Attributes:
        role (Literal["human", "assistant"]): 
            The role of the sender, either "human" or "assistant".
        content (str): 
            The content of the message.
    """
    role: Literal["human", "assistant"]
    content: str
