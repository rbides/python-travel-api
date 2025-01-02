from enum import Enum


class Roles(str, Enum):
    ADMIN = "ADMIN"
    BASIC = "BASIC"

class Permissions(str, Enum):
    TRAVEL_WRITE = "travels:write"
    TRAVEL_DELETE = "travels:delete"