"""Module defines prompts to feed it to gemini"""

CANDID_PROMPT = """\
    Please provide a dictionary extracted from this CV in the following format:
    {
    "bio": "<str: A brief biography of the candidate>",
    "name": "<str>",
    "email": "<str>",
    "educations":[{"title": "<str>", "school": <str>, "start_date":<Date>, "end_date": <Date>}],
    "languages": [<str>],
    "contact_info": {"address": <str>, "linkedin": <str>, "github": <str>, "phone": <str>, "whatsapp": <str>},
    "major": "<str: Major field of study of the candidate>",
    "skills": ["<str: Skill 1>", "<str: Skill 2>", "..."],
    "experiences": [
        {
            "title": "<str: Job title>",
            "company": "<str: Company name>",
            "start_date": "<str: Start date in '%Y-%m-%dT%H:%M:%S.%f' format>",
            "end_date": "<str: End date in '%Y-%m-%dT%H:%M:%S.%f' format>",
            "location": "<str: Location of the job>",
            "description": "<str: Job description>"
        },
    ],
    "languages": ["<str: Language name 1>", "<str: Language name 2>", "..."]
    }

    Notes:
    - Enclose each property in double quotes.
    - The 'start_date' and 'end_date' should respect the format '%Y-%m-%dT%H:%M:%S.%f'.
    - If the 'end_date' is 'present' set it to the current date.
    - Each language should be represented by a string containing the language name.
    """

JOB_PROMPT = """\
    Please extract the following information from this job description and provide it in the form of a dictionary:
    {
      "job_title": "<str: The title of the job>",
      "major": "<str: The major field of study required for the job>",
      "exper_years": "<str: The number of years of experience required>",
      "skills": ["<str: Skill 1>", "<str: Skill 2>", "..."],
      "location": "<str: The location of the job>",
      "job_description": "<str: A detailed description of the job>",
      "application_deadline": "<str: The last date to apply for the job in ISO 8601 format>"
    }

    Notes:
    - Please enclose each property in double quotes.
    - The 'skills' should be represented as lists of strings, each string being a separate skill.
    - If the 'major' is not mentioned explicit try to understand the job and select a suitable major.
    - The 'application_deadline' should be represented as a string in ISO 8601 format (e.g., "2024-05-11T08:06:13.000000") if Not specified set its value to 'None'.
    - If a particular piece of information is not available in the job description, please set its value to 'None'.
    """

ATS_FRIENDLY_PROMPT = """\
    As a professional applicant tracking system, please provide a detailed analysis of this CV. The analysis should include:
    {
    "ats_score": "<float: ATS friendliness score between 0.0 and 1.0>",
    "suggestions": ["<str: Suggestion 1>", "<str: Suggestion 2>", "..."],
    }

    Notes:
    - the input is provided in raw text don't mention any suggestion about fonts style or design.
    - your response criteria based on these tag lines (profile summary or about me, education, work experience, skills, languages, contact information).
    - 'ats_score' should be a float between 0.0 and 1.0, where 1.0 means the CV is perfectly ATS-friendly and 0.0 means it's not ATS-friendly at all.
    - 'suggestions' should be a list of suggestions based on the above criteria for improving the CV to make it more ATS-friendly.
    """

JOB_MATCHING_PROMPT = """\
    Given the candidate's experiences and skills and the job's description and skills,
    please provide a match score between 0.0 and 1.0, where 1.0 means a perfect match
    and 0.0 means no match at all. 

    Please consider the following factors as particularly important: 
    - Relevant skills
    - Years of experience in the relevant field
    - Alignment with the job description

    For example, a perfect match (1.0) might be a candidate who has all the required skills, 
    several years of experience in the field, and whose experiences align closely with the job description. 
    A poor match (0.0) might be a candidate who lacks the required skills and has no relevant experience.
    """
