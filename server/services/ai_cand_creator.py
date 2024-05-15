"""Create a Candidate Profile by Extracting the data using AI"""
from datetime import datetime

from dateutil.parser import parse
from marshmallow import ValidationError

from server.controllers.candidate_controller import CandidateController
from server.controllers.education_controller import EducationController
from server.controllers.language_controller import LanguageController
from server.controllers.schemas import education_schema, work_experience_schema
from server.controllers.skill_controller import SkillController
from server.controllers.user_controller import UserController
from server.controllers.work_experience_controller import WorkExperienceController


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
        self.skill_controller = SkillController()
        self.work_experience_controller = WorkExperienceController()
        self.language_controller = LanguageController()
        self.education_controller = EducationController()

    def create_profile(self):
        """
        Extracts and validates data, updates User and Candidate, adds Skills,
        Languages and Work Experiences, and saves the changes to the storage.
        """
        # Extract and validate data
        try:
            self._extract_data()
            # self._validate_data()
            print("------validation success------->")
        except ValidationError as err:
            print("------validation error(create_profile)------->")
            raise ValueError(err.messages)

        # Update User and Candidate
        user = self._update_user()
        candidate = self._update_candidate(user)

        # Add Skills, Languages and Work Experiences
        self._add_skills(candidate)
        self._add_languages(candidate)
        self._add_work_experiences(candidate)
        self._add_educations(candidate)

        return candidate

    def parse_date(self, date_string):
        """Try to parse the start and end date for experience"""
        try:
            # Try to parse the date string using dateutil.parser.parse
            return parse(date_string).isoformat()
        except ValueError:
            pass

        if date_string.lower() == "present":
            return datetime.now().isoformat()

        return date_string

    def _extract_data(self):
        """Extracts data from the AI data"""
        self.bio = self.ai_data.get("bio")
        self.contact_info = self.ai_data.get("contact_info", None)
        self.skills = self.ai_data.get("skills", [])
        self.languages = self.ai_data.get("languages", [])
        self.experiences = self.ai_data.get("experiences", [])
        self.educations = self.ai_data.get("educations", [])

        # Define a helper function to handle date conversion and missing fields
        def process_fields(data, date_fields, missing_fields):
            for item in data:
                for date_field in date_fields:
                    parsed_date = self.parse_date(item.get(date_field))
                    if parsed_date is not None:
                        item[date_field] = parsed_date
                for missing_field, default_value in missing_fields.items():
                    if item.get(missing_field) is None:
                        item[missing_field] = default_value

        # Convert start_date and end_date to datetime valid
        # strings and handle missing fields
        process_fields(
            self.educations,
            ["start_date", "end_date"],
            {
                "field_of_study": "Not specified",
                "description": "Not specified"
                },
        )
        process_fields(
            self.experiences,
            ["start_date", "end_date"],
            {"location": "Not specified"}
        )

    def _validate_data(self):
        """Validates the extracted data"""
        for experience in self.experiences:
            work_experience_schema.load(experience)

        for education in self.educations:
            education_schema.load(education)

    def _update_user(self):
        """Updates the user data"""
        user_data = {"bio": self.bio, "contact_info": self.contact_info}
        return self.user_controller.update_current_user(
                self.user_id,
                user_data
                )

    def _update_candidate(self, user):
        """Updates the candidate data"""
        return self.candidate_controller.get_current_candidate(user.id)

    def _add_skills(self, candidate):
        """Adds skills to the candidate"""
        for skill_name in self.skills:
            try:
                skill = self.skill_controller.create_skill(
                        {"name": skill_name}
                        )
            except Exception as e:
                continue
            self.candidate_controller.add_skill(candidate.user_id, skill.id)

    def _add_languages(self, candidate):
        """Adds languages to the candidate"""
        for language_name in self.languages:
            try:
                language = self.language_controller.create_language(
                    self.user_id, {"name": language_name}
                )
            except Exception as e:
                continue
            self.candidate_controller.add_language(
                    candidate.user_id,
                    language.id
                    )

    def _add_work_experiences(self, candidate):
        """Adds work experiences to the candidate"""
        for experience_data in self.experiences:
            self.work_experience_controller.create_work_experience(
                candidate.user_id, experience_data
            )

    def _add_educations(self, candidate):
        """Adds educations to the candidate"""
        for education_data in self.educations:
            self.education_controller.create_education(
                    candidate.id,
                    education_data
                    )
