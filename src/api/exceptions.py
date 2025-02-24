from dataclasses import dataclass


@dataclass
class APIError(Exception):
    message: str
    status: int
