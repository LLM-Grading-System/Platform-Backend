from dataclasses import dataclass


@dataclass
class StudentAlreadyExistError(Exception):
    message: str
