from dataclasses import dataclass


@dataclass
class DomainError(Exception):
    status_code: int
    code: str
    message: str


class UnauthorizedError(DomainError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(status_code=401, code="UNAUTHORIZED", message=message)


class ForbiddenError(DomainError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(status_code=403, code="FORBIDDEN", message=message)


class NotFoundError(DomainError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(status_code=404, code="NOT_FOUND", message=message)


class ConflictError(DomainError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(status_code=409, code="CONFLICT", message=message)
