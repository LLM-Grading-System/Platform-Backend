from dataclasses import dataclass


@dataclass
class ServiceError(Exception):
    message: str


@dataclass
class NotFoundError(ServiceError):
    ...


@dataclass
class AlreadyExistError(ServiceError):
    ...

@dataclass
class InvalidPropertyError(ServiceError):
    ...
