from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenDTO:
    token: str


@dataclass
class UserDTO:
    user_id: str
    login: str
    role: str
    created_at: datetime
