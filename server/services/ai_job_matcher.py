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

        Concatenate the candidate's experiences and skills and the job's
        description and skills into one text, add a prompt to tell the AI
        to make the comparison, and return a match_score.

        Returns:
            float: The match score.
        """
        candidate_experiences = " ".join(
            [exp.description for exp in self.candidate.experiences]
        )
        candidate_skills = " ".join(
                [skill.name for skill in self.candidate.skills]
                )
        candidate_info = candidate_experiences + " " + candidate_skills

        job_skills = " ".join([skill.name for skill in self.job.skills])
        job_info = self.job.job_description + " " + job_skills

        combined_info = candidate_info + " " + job_info

        # Ask the AI to calculate the match score
        match_score = self.ai.prompt(JOB_MATCHING_PROMPT, combined_info)

        return match_score
