from enum import Enum

class UserType(Enum):
    OWNER = 'owner'
    MEMBER = 'member'

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.capitalize()) for choice in cls]

PAGE_SIZE = 5