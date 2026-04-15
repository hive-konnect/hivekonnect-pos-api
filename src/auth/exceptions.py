from src.core.errors import ConflictError, UnauthorizedError


class UserAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__("User with this email already exists")


class InvalidCredentials(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")
