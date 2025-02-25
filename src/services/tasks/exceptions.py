from dataclasses import dataclass


@dataclass
class NoTaskError(Exception):
    message: str


@dataclass
class SuchGitHubURLTaskExistError(Exception):
    message: str


@dataclass
class NoCriteriaError(Exception):
    message: str
