"""Create a Job by Extracting the data using AI"""

from datetime import datetime, timezone

from marshmallow import ValidationError

from server.controllers.job_controller import JobController
from server.controllers.major_controller import MajorController
from server.controllers.schemas import job_schema
from server.controllers.skill_controller import SkillController


class AIJobCreator:
    """
    A class used to create a job using AI data.

    Attributes
    ----------
    user_id : str
        a string representing the user's ID
    ai_data : dict
        a dictionary containing the AI data
    job_controller : JobController
        an instance of the JobController class
    major_controller : MajorController
        an instance of the MajorController class
    skill_controller : SkillController
        an instance of the SkillController class
    """

    def __init__(self, user_id, ai_data):
        self.user_id = user_id
        self.ai_data = ai_data
        self.job_controller = JobController()
        self.major_controller = MajorController()
        self.skill_controller = SkillController()

    def parse_date(self, date_string):
        """Try to parse the application_deadline"""
        formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                pass
        # If all formats fail, return None
        return None

    def create_job(self):
        """
        Extracts and validates data, creates a new Job, adds Skills,
        and saves the changes to the storage.
        """
        # Extract skills from the AI data
        skills = self.ai_data.pop("skills", [])

        # Parse application_deadline into a datetime object
        # 'None', None, 'Not specified'
        if "application_deadline" in self.ai_data and self.ai_data[
            "application_deadline"
        ] in (None, "None", "Not specified"):
            del self.ai_data["application_deadline"]

        if "application_deadline" in self.ai_data:
            self.ai_data["application_deadline"] = self.parse_date(
                self.ai_data["application_deadline"]
            )

        print("----job ai------->", self.ai_data)
        # Validate data
        try:
            self.ai_data = job_schema.load(self.ai_data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Create new job
        new_job = self.job_controller.create_job(self.user_id, self.ai_data)

        # Add Skills
        self._add_skills(new_job, skills)
        return new_job

    def _add_skills(self, job, skills):
        """Adds skills to the job"""
        for skill_name in skills:
            skill = self.skill_controller.create_skill({"name": skill_name})
            self.job_controller.add_skill(self.user_id, job.id, skill.id)
