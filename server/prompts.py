"""Module defines prompts to feed it to gemini"""

CANDID_PROMPT = """\
    Please provide a dictionary extracted from this CV in the following format:
    {
    "bio": "<str: A brief biography of the candidate>",
    "contact_info": "<str: Contact information of the candidate>",
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
    "..."
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
    give me a dictionary from this job in the form of:
    {
      title,
      major,
      years_of_experience,
      responsibilites:[],
      skills:[],
      location,
      job_desc:''
    }
    Notes:
    - don't forget to enclose each property in double quotes
"""
