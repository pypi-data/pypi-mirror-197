"""API model exceptions."""


class ModelError(Exception):
    """Base for all API Model issues."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        Exception.__init__(self)

        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class CrudRouterConfigError(ModelError):
    """Raised when CRUD API Router cannot be initialized."""
    pass
