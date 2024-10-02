"""
This module provides a controller for the Skill model in the
Job-linker application.
"""

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.controllers.schemas import skill_schema
from server.models import storage
from server.models.skill import Skill
from server.skill_synonyms import SKILL_SYNONYMS


class SkillController:
    """
    Controller for Skill model.
    """

    def __init__(self):
        """
        Initializes the SkillController.
        """
        pass

    def get_skills(self):
        """
        Fetches all skills.

        Returns:
            A list of all skills.
        """
        skills = storage.all(Skill).values()
        return skills

    def create_skill(self, data):
        """
        Creates a new skill.

        Args:
            data: The data of the skill to be created.

        Returns:
            The created skill.

        Raises:
            ValueError: If there is a validation error or the skill
            name already exists.
        """
        # Validate data
        try:
            data = skill_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if skill name is a synonym and replace it
        # with the canonical name
        skill_name = data["name"]
        canonical_name = SKILL_SYNONYMS.get(skill_name, skill_name)
        data["name"] = canonical_name

        # Check if skill already exists
        existing_skill = storage.get_by_attr(Skill, "name", data["name"])
        if existing_skill:
            return existing_skill

        # Create new skill
        new_skill = Skill(name=data["name"])
        storage.new(new_skill)
        try:
            storage.save()
        except IntegrityError:
            raise ValueError("Skill name already exists")

        return new_skill

    def update_skill(self, skill_id, data):
        """
        Updates a specific skill.

        Args:
            skill_id: The ID of the skill.
            data: The data to update the skill with.

        Returns:
            The updated skill.

        Raises:
            ValueError: If there is a validation error, the skill is not found
            , or the skill name already exists.
        """
        # Validate data
        try:
            data = skill_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Get skill and update attributes
        skill = storage.get(Skill, skill_id)
        if not skill:
            raise ValueError("Skill not found")

        for key, value in data.items():
            setattr(skill, key, value)
        try:
            storage.save()
        except IntegrityError:
            raise ValueError("Skill name already exists")

        return skill

    def delete_skill(self, skill_id):
        """
        Deletes a specific skill.

        Args:
            skill_id: The ID of the skill.

        Raises:
            ValueError: If the skill is not found.
        """
        # Get skill
        skill = storage.get(Skill, skill_id)
        if not skill:
            raise ValueError("Skill not found")

        # Delete skill
        storage.delete(skill)
        storage.save()
