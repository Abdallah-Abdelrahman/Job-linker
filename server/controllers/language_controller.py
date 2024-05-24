"""
This module provides a controller for the Language model in the
Job-linker application.
"""

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.controllers.schemas import language_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.language import Language
from server.models.user import User


class LanguageController:
    """
    Controller for Language model.
    """

    def __init__(self):
        """
        Initializes the LanguageController.
        """
        pass

    def get_languages(self):
        """
        Fetches all languages.

        Returns:
            A list of all languages.
        """
        languages = storage.all(Language).values()
        return languages

    def create_language(self, user_id, data):
        """
        Creates a new language.

        Args:
            user_id: The ID of the user.
            data: The data of the language to be created.

        Returns:
            The created language.

        Raises:
            ValueError: If there is a validation error or the language name
            already exists.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Validate data
        try:
            data = language_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        user = storage.get(User, user_id)
        if not user:
            raise UnauthorizedError("Unauthorized")

        # Check if language already exists
        existing_language = storage.get_by_attr(Language, "name", data["name"])
        if existing_language:
            return existing_language

        # Create new language
        new_language = Language(name=data["name"])
        storage.new(new_language)
        try:
            storage.save()
        except IntegrityError:
            raise ValueError("Language name already exists")

        return new_language

    def update_language(self, user_id, language_id, data):
        """
        Updates a specific language.

        Args:
            user_id: The ID of the user.
            language_id: The ID of the language.
            data: The data to update the language with.

        Returns:
            The updated language.

        Raises:
            ValueError: If there is a validation error, the language is not
            found, or the language name already exists.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Validate data
        try:
            data = language_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        user = storage.get(User, user_id)
        if not user:
            raise UnauthorizedError("Unauthorized")

        # Get language and update attributes
        language = storage.get(Language, language_id)
        if not language:
            raise ValueError("Language not found")

        for key, value in data.items():
            setattr(language, key, value)
        try:
            storage.save()
        except IntegrityError:
            raise ValueError("Language name already exists")

        return language

    def delete_language(self, user_id, language_id):
        """
        Deletes a specific language.

        Args:
            user_id: The ID of the user.
            language_id: The ID of the language.

        Raises:
            ValueError: If the language is not found.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Check if user is a recruiter
        user = storage.get(User, user_id)
        if not user or user.role != "recruiter":
            raise UnauthorizedError("Unauthorized")

        # Get language
        language = storage.get(Language, language_id)
        if not language:
            raise ValueError("Language not found")

        # Delete language
        storage.delete(language)
        storage.save()
