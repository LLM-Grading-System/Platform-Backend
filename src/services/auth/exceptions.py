from dataclasses import dataclass


@dataclass
class NoUserError(Exception):
    message: str


@dataclass
class UserAlreadyExistError(Exception):
    message: str


@dataclass
class InvalidPasswordError(Exception):
    message: str
