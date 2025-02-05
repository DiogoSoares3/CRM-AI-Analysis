from pydantic import BaseModel, NonNegativeInt

class ExampleSchema(BaseModel):
    """
    Represents an example data schema.

    Attributes:
        name (str): 
            The name of the example entity.
        description (str | None): 
            A brief description of the entity (can be None).
        date (str | None): 
            The associated date in string format (can be None).
    """
    name: str
    description: str | None
    date: str | None

class Message(BaseModel):
    """
    Represents a user message containing a query and a reference to message history.

    Attributes:
        message_history_id (NonNegativeInt): 
            A non-negative integer representing the message history ID.
        query (str): 
            The content of the query sent by the user.
    """
    message_history_id: NonNegativeInt
    query: str
