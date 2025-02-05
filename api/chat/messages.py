from enum import Enum, auto
from pydantic import BaseModel

class RoleNotRecognized(Exception):
    """
    Exception raised when a provided role is not recognized.

    Args:
        role_provided (str):
            The role that was provided but not recognized.
        roles_availables (list[list[str]]):
            The available role equivalents categorized.

    Attributes:
        role_provided (str):
            Stores the unrecognized role.
        roles_availables (list[list[str]]):
            Stores the available role mappings.

    Methods:
        __str__():
            Returns a descriptive error message.
    """
    def __init__(self, role_provided: str, roles_availables: list[list[str]]):
        self.role_provided = role_provided
        self.roles_availables = roles_availables

    def __str__(self) -> str:
        return (f"Role provided ({self.role_provided}) not in available roles "
                f"({self.roles_availables}), provide an entity mapper")


class Role(Enum):
    """
    Enum representing different roles in a chat system.

    Roles:
        assistant: Represents an AI assistant.
        human: Represents a human user.
        system: Represents a system-generated message.

    Methods:
        get(role: str) -> Role:
            Returns the corresponding Role enum based on the provided role string.
    """
    assistant = auto()
    human = auto()
    system = auto()

    @staticmethod
    def get(role: str) -> 'Role':
        """
        Maps a string representation of a role to the corresponding Role enum.

        Args:
            role (str):
                The string representation of the role.

        Returns:
            Role:
                The corresponding Role enum.

        Raises:
            RoleNotRecognized:
                If the provided role does not match any known equivalents.
        """
        role = role.lower()
        human_equivalents = ['human', 'user']
        system_equivalents = ['system', 'sys']
        assistant_equivalents = ['assistant', 'ai']

        if role in human_equivalents:
            return Role.human
        if role in assistant_equivalents:
            return Role.assistant
        if role in system_equivalents:
            return Role.system

        raise RoleNotRecognized(
                role_provided=role,
                roles_availables=[human_equivalents,
                                  system_equivalents,
                                  assistant_equivalents])

class Message(BaseModel):
    """
    Represents a message in the chat system.

    Args:
        role (Role):
            The role of the sender (assistant, human, or system).
        content (str):
            The message content.

    Attributes:
        role (Role):
            The sender's role.
        content (str):
            The message content.
    """
    role: Role
    content: str

class MessageHistory:
    """
    Maintains a history of messages in a chat.

    Attributes:
        message_history (list[Message]):
            A list storing all messages in the chat history.

    Methods:
        add_message(message: Message) -> None:
            Adds a message to the history.
        add_human_message(content: str) -> None:
            Adds a message from a human user.
        add_system_message(content: str) -> None:
            Adds a system-generated message.
        add_assistant_message(content: str) -> None:
            Adds a message from the assistant.
    """
    def __init__(self):
        """
        Initializes an empty message history.
        """
        self.message_history: list[Message] = []

    def add_message(self, message: Message) -> None:
        """
        Adds a message to the history.

        Args:
            message (Message):
                The message to be added.
        """
        self.message_history.append(message)

    def add_human_message(self, content: str) -> None:
        """
        Adds a message from a human user.

        Args:
            content (str):
                The message content.
        """
        message = Message(role=Role.human, content=content)
        self.message_history.append(message)

    def add_system_message(self, content: str) -> None:
        """
        Adds a system-generated message.

        Args:
            content (str):
                The message content.
        """
        message = Message(role=Role.system, content=content)
        self.message_history.append(message)

    def add_assistant_message(self, content: str) -> None:
        """
        Adds a message from the assistant.

        Args:
            content (str):
                The message content.
        """
        message = Message(role=Role.assistant, content=content)
        self.message_history.append(message)
