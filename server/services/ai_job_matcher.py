"""Calculat the match between applied Candidate and Job using AI"""


from server.prompts import JOB_MATCHING_PROMPT
from server.services.ai import AIService


class AIJobMatcher:
    """
    A class used to match a candidate with a job using AI.

    Attributes
    ----------
    candidate : Candidate
        The candidate to be matched.
    job : Job
        The job to match the candidate with.
    ai : AIService
        The AI service used for matching.
    """

    def __init__(self, candidate, job):
        self.candidate = candidate
        self.job = job
        self.ai = AIService()

    def calculate_match_score(self):
        """
        Calculate the match score between the candidate and the job.

        Concatenate the candidate's experiences, skills, and education and
        the job's description, skills, and responsibilities into one text,
        add a prompt to tell the AI to make the comparison, and return a
        match_score.

        Returns:
            float: The match score.
        """
        candidate_experiences = " ".join(
            [exp.description for exp in self.candidate.experiences]
        )
        candidate_skills = " ".join(
                [skill.name for skill in self.candidate.skills]
                )

        candidate_education = " ".join(
            [
                f"{edu.degree} in {edu.field_of_study} from {edu.description}"
                for edu in self.candidate.educations
            ]
        )

        candidate_info = (
            "Candidate's experiences, skills, and education:"
            + candidate_experiences
            + " "
            + candidate_skills
            + " "
            + candidate_education
        )

        job_skills = " ".join([skill.name for skill in self.job.skills])
        job_responsibilities = " ".join(self.job.responsibilities)
        job_info = (
            "Job's description, required skills, and responsibilities:"
            + self.job.job_description
            + " "
            + job_skills
            + " "
            + job_responsibilities
        )

        combined_info = candidate_info + " " + job_info

        # Ask the AI to calculate the match score
        match_score = self.ai.prompt(JOB_MATCHING_PROMPT, combined_info)

        return match_score
