from pydantic import BaseModel
from typing import Literal

class SQLInjectionStatus(BaseModel):
    status: Literal["Insecure", "Secure"]

class SerializableChatSchema(BaseModel):
    role: Literal["human", "assistant"]
    content: str
