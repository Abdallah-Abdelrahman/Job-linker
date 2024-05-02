"""
This module provides a controller for the Administrator view
in the Job-linker application.
"""

from flask import g

from server.exception import UnauthorizedError
from server.models import storage
from server.models.application import Application
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.language import Language
from server.models.major import Major
from server.models.recruiter import Recruiter
from server.models.skill import Skill
from server.models.user import User
from server.models.work_experience import WorkExperience


class AdminController:
    """
    Controller for handling operations related to admin users.
    """

    def __init__(self):
        """
        Initializes the AdminController.
        """
        pass

    def _check_admin(self):
        """Check if the user is authenticated and is an admin."""
        if g.user is None:
            raise UnauthorizedError("User is not authenticated")
        if not g.user.is_admin:
            raise UnauthorizedError("Unauthorized")

    def get_all_users(self):
        """
        Fetches all users in the system.

        This method should only be accessible by admin users.

        Raises:
            UnauthorizedError: If the current user is not an admin.

        Returns:
            list: A list of all users.
        """
        self._check_admin()

        users = storage.all(User).values()
        return users

    def delete_user(self, user_id):
        """
        Deletes a specific user from the system.

        This method should only be accessible by admin users.

        Args:
            user_id (str): The ID of the user to delete.

        Raises:
            UnauthorizedError: If the current user is not an admin.
        """
        self._check_admin()

        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found.")

        storage.delete(user)
        storage.save()

    def disable_user(self, user_id):
        """
        Disables a specific user account.

        This method should only be accessible by admin users.

        Args:
            user_id (str): The ID of the user to disable.

        Raises:
            UnauthorizedError: If the current user is not an admin.
        """
        self._check_admin()

        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found.")

        user.verified = False
        storage.save()

    def enable_user(self, user_id):
        """
        Enables a specific user account.

        This method should only be accessible by admin users.

        Args:
            user_id (str): The ID of the user to enable.

        Raises:
            UnauthorizedError: If the current user is not an admin.
        """
        self._check_admin()

        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found.")

        user.verified = True
        storage.save()

    def change_user_role(self, user_id, new_role):
        """
        Changes the role of a specific user.

        This method should only be accessible by admin users.

        Args:
            user_id (str): The ID of the user.
            new_role (str): The new role for the user.

        Raises:
            UnauthorizedError: If the current user is not an admin.
        """
        self._check_admin()

        valid_roles = ["candidate", "recruiter"]
        if new_role not in valid_roles:
            raise ValueError(
                f"Invalid role '{new_role}'. "
                f"Role must be one of {valid_roles}."
            )

        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found.")

        user.role = new_role
        storage.save()

    def get_sys_statistics(self):
        """
        Fetches system statistics.

        This method should only be accessible by admin users.

        Raises:
            UnauthorizedError: If the current user is not an admin.

        Returns:
            Dict: A count of all users, recruiters, candidates, jobs,
            applications, languages, skills, majors, and work experiences.
        """
        self._check_admin()

        models = {
            "total_users": User,
            "total_recruiters": Recruiter,
            "total_candidates": Candidate,
            "total_jobs": Job,
            "total_applications": Application,
            "total_languages": Language,
            "total_skills": Skill,
            "total_majors": Major,
            "total_work_experiences": WorkExperience,
        }

        return {name: storage.count(model) for name, model in models.items()}
