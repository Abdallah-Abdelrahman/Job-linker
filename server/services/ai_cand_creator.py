"""Create a Candidate Profile by Extracting the data using AI"""
from datetime import datetime
from json import dumps
from marshmallow import ValidationError

from server.controllers.candidate_controller import CandidateController
from server.controllers.schemas import work_experience_schema
from server.controllers.user_controller import UserController
from server.models import storage
from server.models.candidate import Candidate
from server.models.language import Language
from server.models.skill import Skill
from server.models.user import User
from server.models.work_experience import WorkExperience


class AICandidateProfileCreator:
    """
    A class used to create a candidate profile using AI data.

    ...

    Attributes
    ----------
    user_id : str
        a string representing the user's ID
    ai_data : dict
        a dictionary containing the AI data
    user_controller : UserController
        an instance of the UserController class
    candidate_controller : CandidateController
        an instance of the CandidateController class
    """

    def __init__(self, user_id, ai_data, bcrypt_instance):
        self.user_id = user_id
        self.ai_data = ai_data
        self.user_controller = UserController(bcrypt_instance)
        self.candidate_controller = CandidateController()

    def create_profile(self):
        """
        Extracts and validates data, updates User and Candidate, adds Skills,
        Languages and Work Experiences, and saves the changes to the storage.
        """
        # Extract and validate data
        try:
            self._extract_data()
            #self._validate_data()
            print('------validation success------->')
        except ValidationError as err:
            print('------validation error(create_profile)------->')
            raise ValueError(err.messages)

        # Update User and Candidate
        user = self._update_user()
        candidate = self._update_candidate(user)

        # Add Skills, Languages and Work Experiences
        self._add_skills(candidate)
        self._add_languages(candidate)
        self._add_work_experiences(candidate)

        storage.save()
        return candidate

    def parse_date(self, date_string):
        """Try to parse the start and end date for experience"""
        formats = ["%d/%m/%Y", "%m/%Y", "%Y-%m-%dT%H:%M:%S.%f"]
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt).isoformat()
            except ValueError:
                pass

        if len(date_string.split("/")) == 2:
            date_string = "01/" + date_string
            return datetime.strptime(date_string, "%d/%m/%Y").isoformat()

        if date_string.lower() == "present":
            return datetime.now().isoformat()

        if date_string.startswith("2024-"):
            try:
                year = int(date_string.split("-")[0])
                return datetime(year=year, month=1, day=1).isoformat()
            except ValueError:
                pass

    def _extract_data(self):
        """Extracts data from the AI data"""
        self.bio = self.ai_data.get("bio")
        contact_info = self.ai_data.get("contact_info")
        if contact_info is not None:
            self.contact_info = contact_info
            print('-----JSON CONTANCT------->', self.contact_info)
        else:
            self.contact_info = None
        self.skills = self.ai_data.get("skills", [])
        self.languages = self.ai_data.get("languages", [])
        self.experiences = self.ai_data.get("experiences", [])

        # Convert start_date and end_date to datetime objects
        for experience in self.experiences:
            for date_field in ["start_date", "end_date"]:
                if date_field in experience:
                    if experience[date_field] is not None:
                        date_obj = self.parse_date(experience[date_field])
                        if date_obj is not None:
                            experience[date_field] = date_obj
                    else:
                        if date_field == "end_date":
                            experience[date_field] = datetime.now().isoformat()
                # Convert location to string
                if "location" in experience:
                    if experience["location"] is not None:
                        experience["location"] = str(experience["location"])

    def _validate_data(self):
        """Validates the extracted data"""
        for experience in self.experiences:
            work_experience_schema.load(experience)

    def _update_user(self):
        """Updates the user data"""
        user_data = {"bio": self.bio, "contact_info": self.contact_info}
        user = storage.get(User, self.user_id)
        if user:
            return self.user_controller.update_current_user(
                    self.user_id,
                    user_data
                    )
        else:
            raise ValueError("User not found")

    def _update_candidate(self, user):
        """Updates the candidate data"""
        candidate = storage.get_by_attr(Candidate, "user_id", user.id)
        if candidate:
            return candidate
        else:
            raise ValueError("Candidate not found")

    def _add_skills(self, candidate):
        """Adds skills to the candidate"""
        for skill_name in self.skills:
            skill = storage.get_by_attr(Skill, "name", skill_name)
            if not skill:
                skill = Skill(name=skill_name)
                storage.new(skill)
            candidate.skills.append(skill)

    def _add_languages(self, candidate):
        """Adds languages to the candidate"""
        for language_name in self.languages:
            language = storage.get_by_attr(Language, "name", language_name)
            if not language:
                language = Language(name=language_name)
                storage.new(language)
            candidate.languages.append(language)

    def _add_work_experiences(self, candidate):
        """Adds work experiences to the candidate"""
        for experience_data in self.experiences:
            experience = WorkExperience(
                    candidate_id=candidate.id,
                    **experience_data
                    )
            storage.new(experience)
