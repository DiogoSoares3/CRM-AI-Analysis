from enum import Enum, auto

from pydantic import BaseModel

class RoleNotRecognized(Exception):
    def __init__(self, role_provided, roles_availables):
        self.role_provided = role_provided
        self.roles_availables = roles_availables

    def __str__(self):
        return (f"Role provided ({self.role_provided}) not in available roles "
                f"({self.roles_availables}), provide an entity mapper")

class Role(Enum):
    assistant = auto()
    human = auto()
    system = auto()

    def get(role: str):
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
    role: Role
    content: str

class MessageHistory:
    def __init__(self):
        self.message_history = []

    def add_message(self, message: Message):
        self.message_history.append(message)

    def add_human_message(self, content: str):
        message = Message(role=Role.human, content=content)
        self.message_history.append(message)

    def add_system_message(self, content: str):
        message = Message(role=Role.system, content=content)
        self.message_history.append(message)

    def add_assistant_message(self, content: str):
        message = Message(role=Role.assistant, content=content)
        self.message_history.append(message)
