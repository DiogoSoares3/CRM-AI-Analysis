from pydantic import BaseModel, NonNegativeInt

class ExampleSchema(BaseModel):
    name: str
    description: str | None
    date: str | None

class Message(BaseModel):
    message_history_id: NonNegativeInt
    query: str
