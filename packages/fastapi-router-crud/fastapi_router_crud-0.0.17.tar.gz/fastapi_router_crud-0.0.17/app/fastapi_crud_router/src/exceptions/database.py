"""Database exceptions."""


class DatabaseError(Exception):
    """Base for all database issues."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        Exception.__init__(self)

        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class InitError(DatabaseError):
    """Raised when the database cannot be initialized."""
    pass


class CloseError(DatabaseError):
    """Raised when the database cannot be closed."""
    pass