"""Module defines prompts to feed it to gemini"""

CANDID_PROMPT = """\
    Please provide a dictionary extracted from this CV in the following format:
    {
    "bio": "<str: A brief biography of the candidate>",
    "name": "<str>",
    "email": "<str>",
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
    "educations": [
        {
            "institute": "<str: Name of the institute>",
            "degree": "<str: Degree obtained>",
            "field_of_study": "<str: Field of study>",
            "start_date": "<str: Start date in '%Y-%m-%dT%H:%M:%S.%f' format>",
            "end_date": "<str: End date in '%Y-%m-%dT%H:%M:%S.%f' format>",
            "description": "<str: Description of the education>"
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
As a professional data extraction system, please extract the following information from the given job description text. Provide the extracted information in the form of a dictionary with the specified structure:
{
  "job_title": "<str: The title of the job>",
  "exper_years": "<str: The number of years of experience required>",
  "skills": ["<str: Skill 1>", "<str: Skill 2>", "..."],
  "location": "<str: The location of the job>",
  "job_description": "<str: A detailed description of the job>",
  "application_deadline": "<str: The last date to apply for the job in ISO 8601 format>",
  "responsibilities": ["<str: Responsibility 1>", "<str: Responsibility 2>", "..."]
}

Guidelines:
1. Job Title: Extract the job title accurately from the description.
2. Experience Years: Extract the number of years of experience required. If not specified, set the value to 'None'.
3. Skills: Extract the required skills and list them as strings within an array. Each skill should not exceed 100 characters. If not specified, set the value to an empty list.
4. Location: Extract the job location. If not specified, set the value to 'None'.
5. Job Description: Provide a detailed description of the job as mentioned in the text.
6. Application Deadline: Extract the application deadline in ISO 8601 format (e.g., "2024-05-11T08:06:13.000000"). If not specified, set its value to 'None'.
7. Responsibilities: Extract the job responsibilities and list them as strings within an array. Each responsibility should not exceed 200 characters. If not specified, set the value to an empty list.  # Add this line
8. Format: Ensure each property is enclosed in double quotes and the structure of the dictionary is maintained.

Example Response:
{
  "job_title": "Software Engineer",
  "exper_years": "3-5 years",
  "skills": ["Python", "Django", "REST APIs"],
  "location": "New York, NY",
  "job_description": "We are looking for a skilled Software Engineer...",
  "application_deadline": "2024-05-11T08:06:13.000000",
  "responsibilities": ["Develop and maintain software", "Collaborate with cross-functional teams"]  # Add this line
}

Notes:
- If a particular piece of information is not available in the job description, please set its value to 'None'.
- Ensure the extracted information is accurate and corresponds to the details provided in the job description.
"""


ATS_FRIENDLY_PROMPT = """\
As a professional applicant tracking system (ATS) evaluator, please analyze the following CV text and provide a detailed assessment. The analysis should include the following:
{
"ats_score": "<float: ATS friendliness score between 0.0 and 1.0>",
"suggestions": ["<str: Suggestion 1>", "<str: Suggestion 2>", "..."]
}

Guidelines:
1. Input Format: The CV is provided in raw text extracted from a PDF. Do not make any suggestions about font style, size, or design.
2. Evaluation Criteria: Base your analysis on the following sections:
   - Profile Summary/About Me: Clarity, conciseness, relevance, and presence of keywords.
   - Education: Proper formatting, relevance to the job, inclusion of degrees, institutions, and dates.
   - Work Experience: Use of action verbs, quantifiable achievements, relevance, proper formatting (job titles, companies, dates).
   - Skills: Relevance to the job, proper categorization, presence of both hard and soft skills.
   - Languages: Inclusion of languages spoken, proficiency levels.
   - Contact Information: Presence of phone number, email, LinkedIn profile, and other relevant contact details.

3. Scoring:
   - The 'ats_score' should be a float between 0.0 and 1.0, where 1.0 indicates a perfectly ATS-friendly CV and 0.0 indicates it is not ATS-friendly at all.
   - The score should reflect the overall quality and ATS-friendliness based on the provided criteria.

4. Suggestions:
   - Provide specific and actionable suggestions to improve the CV’s ATS-friendliness.
   - Each suggestion should correspond to one of the evaluation criteria mentioned above.
   - Ensure suggestions are clear, concise, and relevant to improving the ATS score.

Example Response:
{
"ats_score": 0.85,
"suggestions": [
    "Improve the profile summary by including more keywords relevant to the job.",
    "Ensure each work experience entry includes quantifiable achievements.",
    "List your skills in a separate section with proper categorization."
]
}
"""

JOB_MATCHING_PROMPT = """\
As an advanced matching system, please evaluate the compatibility between the candidate's experiences and skills and the job's description and required skills. Provide a match score as a float between 0.0 and 1.0, where 1.0 indicates a perfect match and 0.0 indicates no match at all.

Important Factors:
1. Relevant Skills: Evaluate how well the candidate's skills match the required skills for the job.
2. Years of Experience: Consider the candidate's years of experience in the relevant field compared to the job requirements.
3. Alignment with Job Description: Assess how closely the candidate's experiences align with the job description.

Output Format:
- Return only a single float number as the match score.
- Do not provide any descriptive text or additional explanations.

Example:
A candidate who has all the required skills, significant years of relevant experience, and experiences closely aligned with the job description might receive a score close to 1.0. Conversely, a candidate lacking the required skills and relevant experience might receive a score close to 0.0.

Please provide the match score based on the above criteria.
"""
