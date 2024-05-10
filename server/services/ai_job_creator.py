"""Create a Job by Extracting the data using AI"""

from marshmallow import ValidationError

from server.controllers.job_controller import JobController
from server.controllers.schemas import job_schema
from server.models import storage
from server.models.major import Major
from server.models.skill import Skill


class AIJobCreator:
    """
    A class used to create a job using AI data.

    Attributes
    ----------
    recruiter_id : str
        a string representing the recruiter's ID
    ai_data : dict
        a dictionary containing the AI data
    job_controller : JobController
        an instance of the JobController class
    """

    def __init__(self, recruiter_id, ai_data):
        self.recruiter_id = recruiter_id
        self.ai_data = ai_data
        self.job_controller = JobController()

    def create_job(self):
        """
        Extracts and validates data, creates a new Job, adds Skills,
        and saves the changes to the storage.
        """
        # Extract skills and major from the AI data
        skills = self.ai_data.pop("skills", [])
        major_name = self.ai_data.pop("major", None)

        # Get or create the Major
        major = storage.get_by_attr(Major, "name", major_name)
        if not major:
            major = Major(name=major_name)
            storage.new(major)
            storage.save()

        # Add the major_id to the ai_data
        self.ai_data["major_id"] = major.id

        # Validate data
        try:
            self.ai_data = job_schema.load(self.ai_data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Create new job
        new_job = self.job_controller.create_job(
                self.recruiter_id,
                self.ai_data
                )

        # Add Skills
        self._add_skills(new_job, skills)

        storage.save()
        return new_job

    def _add_skills(self, job, skills):
        """Adds skills to the job"""
        for skill_name in skills:
            skill = storage.get_by_attr(Skill, "name", skill_name)
            if not skill:
                skill = Skill(name=skill_name)
                storage.new(skill)
                storage.save()
            job.skills.append(skill)
