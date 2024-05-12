"""
This module provides a controller for the UserFile model in the
Job-linker application.
"""

from server.models import storage
from server.models.user import User
from server.models.user_file import UserFile


class UserFileController:
    """
    Controller for UserFile model.
    """

    def __init__(self):
        """
        Initializes the UserFileController.
        """
        pass

    def create_user_file(self, user_id, filename, original_filename):
        """
        Creates a new user file record.

        Args:
            user_id: The ID of the user.
            filename: The unique filename of the uploaded file.
            original_filename: The original filename of the uploaded file.

        Returns:
            The created user file record.

        Raises:
            ValueError: If the user is not found.
        """
        # Check if user exists
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        # Create new user file record
        new_user_file = UserFile(
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
        )
        storage.new(new_user_file)
        storage.save()

        return new_user_file

    def get_user_files(self, user_id):
        """
        Gets all the user file records for a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of user file records for the specified user.

        Raises:
            ValueError: If the user is not found.
        """
        # Check if user exists
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        # Get user file records
        user_files = storage.get_all_by_attr(UserFile, "user_id", user_id)

        return user_files or []

    def delete_user_file(self, user_id, filename):
        """
        Deletes a user file record.

        Args:
            user_id: The ID of the user.
            filename: The unique filename of the uploaded file.

        Raises:
            ValueError: If the user or user file record is not found.
        """
        # Check if user exists
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        # Get user file record
        user_file = storage.get_by_attr(UserFile, "filename", filename)
        if not user_file or user_file.user_id != user_id:
            raise ValueError("User file record not found")

        # Delete user file record
        storage.delete(user_file)
        storage.save()
