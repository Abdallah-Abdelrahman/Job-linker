"""
This module provides an exception class for unauthorized access in the
Job-linker application.
"""


class UnauthorizedError(Exception):
    """Exception raised for unauthorized access."""

    def __init__(self, message="Unauthorized"):
        """
        Initializes the UnauthorizedError with an optional message.

        Args:
            message: The message to be associated with the exception.
            Defaults to "Unauthorized".
        """
        self.message = message
        super().__init__(self.message)
