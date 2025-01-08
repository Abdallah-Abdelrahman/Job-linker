"""Module defines prompts to feed it to gemini"""

PTA_PROMPT = """\
Please provide a dictionary extracted from this CV in the following format:
{
    "profession": "<str: Profession of the candidate>",
    "age": "<str: Age of the candidate>",
    "intro": "<str: A brief introduction or summary of the candidate>",
    "experiences": [
        {
            "company_name": "<str: Name of the company>",
            "start_date": "<str: Start date in 'YYYY-MM-DD' format>",
            "end_date": "<str: End date in 'YYYY-MM-DD' format>",
            "description": "<str: Description of the role and responsibilities>",
            "job_title": "<str: Job title>"
        },
    ],
    "education": [
        {
            "degree": "<str: Degree obtained>",
            "major": "<str: Major field of study>",
            "university": "<str: Name of the university>",
            "graduate_date": "<str: Graduation date in 'YYYY-MM-DD' format>",
            "gpa": "<float: GPA score>",
            "gpa_from": "<float: GPA scale>"
        },
    ],
    "skills": [
        {
            "name": "<str: Skill name>"
        },
    ],
    "certificates": [
        {
            "name": "<str: Certificate name>"
        },
    ],
    "links": [
        {
            "name": "<str: Name of the link (e.g., LinkedIn, Twitter)>",
            "link": "<str: URL of the link>"
        },
    ]
}

Notes:
1. **Language Handling**:
   - Detect the language of the CV (Arabic or English).
   - Return the extracted information in the same language as the CV.
   - If the CV contains both Arabic and English, prioritize the dominant language.

2. **Formatting**:
   - Enclose each property in double quotes.
   - The 'start_date', 'end_date', and 'graduate_date' should respect the format 'YYYY-MM-DD'.
   - If the 'end_date' is 'present', set it to the current date.

3. **Skills**:
   - Extract the skills listed in the CV.
   - Each skill should be represented as an object with a 'name' property.
   - Each skill name should not exceed 100 characters.

4. **Certificates**:
   - Extract the certificates listed in the CV.
   - Each certificate should be represented as an object with a 'name' property.

5. **Links**:
   - Extract the links (e.g., LinkedIn, Twitter) listed in the CV.
   - Each link should be represented as an object with 'name' and 'link' properties.

6. **Descriptions**:
   - The description for each experience must not include any bullet points. Remove them if any exist in the text.
   - Ensure descriptions are concise and relevant.

7. **Special Cases**:
   - If a field is missing or cannot be extracted, set its value to `null`.
   - Handle Arabic text with proper Unicode encoding (e.g., "العربية" instead of "?????").

Example Output for Arabic CV:
{
    "profession": "مهندس برمجيات",
    "age": "23",
    "intro": "مهندس برمجيات ذو خبرة واسعة في تطوير تطبيقات الويب والهواتف المحمولة.",
    "experiences": [
        {
            "company_name": "شركة التقنية",
            "start_date": "2020-01-01",
            "end_date": "2023-12-31",
            "description": "تطوير تطبيقات الويب باستخدام React وNode.js.",
            "job_title": "مهندس برمجيات"
        },
    ],
    "education": [
        {
            "degree": "بكالوريوس",
            "major": "هندسة البرمجيات",
            "university": "جامعة القاهرة",
            "graduate_date": "2020-06-30",
            "gpa": 3.5,
            "gpa_from": 4.0
        },
    ],
    "skills": [
        {
            "name": "تطوير الويب"
        },
        {
            "name": "React"
        },
        {
            "name": "Node.js"
        }
    ],
    "certificates": [
        {
            "name": "شهادة Scrum"
        },
        {
            "name": "شهادة Odoo"
        }
    ],
    "links": [
        {
            "name": "LinkedIn",
            "link": "linkedin.com/in/example"
        },
        {
            "name": "Twitter",
            "link": "twitter.com/example"
        }
    ]
}

Example Output for English CV:
{
    "profession": "Software Engineer",
    "age": "23",
    "intro": "Software engineer with extensive experience in web and mobile application development.",
    "experiences": [
        {
            "company_name": "Tech Company",
            "start_date": "2020-01-01",
            "end_date": "2023-12-31",
            "description": "Developed web applications using React and Node.js.",
            "job_title": "Software Engineer"
        },
    ],
    "education": [
        {
            "degree": "Bachelor",
            "major": "Software Engineering",
            "university": "Cairo University",
            "graduate_date": "2020-06-30",
            "gpa": 3.5,
            "gpa_from": 4.0
        },
    ],
    "skills": [
        {
            "name": "Web Development"
        },
        {
            "name": "React"
        },
        {
            "name": "Node.js"
        }
    ],
    "certificates": [
        {
            "name": "Scrum Certification"
        },
        {
            "name": "Odoo Certification"
        }
    ],
    "links": [
        {
            "name": "LinkedIn",
            "link": "linkedin.com/in/example"
        },
        {
            "name": "Twitter",
            "link": "twitter.com/example"
        }
    ]
}
"""

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
1. **Language Handling**:
   - Detect the language of the CV (Arabic or English).
   - Return the extracted information in the same language as the CV.
   - The headlines like bio, experience, education, etc., might be written in arabic beware that.

2. **Formatting**:
   - Enclose each property in double quotes.
   - The 'start_date' and 'end_date' should respect the format '%Y-%m-%dT%H:%M:%S.%f'.
   - If the 'end_date' is 'present', set it to the current date.

3. **Skills**:
   - Extract the skills listed in the CV.
   - Each skill should be represented by a string and listed in an array.
   - Each skill should not exceed 100 characters.

4. **Languages**:
   - Each language should be represented by a string containing the language name.
   - If the CV is in Arabic, return language names in Arabic (e.g., "العربية" for Arabic, "الإنجليزية" for English).
   - If the CV is in English, return language names in English (e.g., "Arabic", "English").

5. **Descriptions**:
   - The description for each experience must not include any bullet points. Remove them if any exist in the text.
   - Ensure descriptions are concise and relevant.

6. **Special Cases**:
   - If a field is missing or cannot be extracted, set its value to `null`.
   - Handle Arabic text with proper Unicode encoding (e.g., "العربية" instead of "?????").

Example Output for Arabic CV:
{
    "bio": "مهندس برمجيات ذو خبرة واسعة في تطوير تطبيقات الويب والهواتف المحمولة.",
    "name": "محمد أحمد",
    "email": "mohamed.ahmed@example.com",
    "contact_info": {"address": "القاهرة، مصر", "linkedin": "linkedin.com/in/mohamed-ahmed", "github": "github.com/mohamed-ahmed", "phone": "+201234567890", "whatsapp": "+201234567890"},
    "major": "هندسة البرمجيات",
    "skills": ["تطوير الويب", "تطبيقات الهواتف", "قواعد البيانات"],
    "experiences": [
        {
            "title": "مهندس برمجيات",
            "company": "شركة التقنية",
            "start_date": "2020-01-01T00:00:00.000",
            "end_date": "2023-12-31T00:00:00.000",
            "location": "القاهرة، مصر",
            "description": "تطوير تطبيقات الويب باستخدام React وNode.js."
        },
    ],
    "educations": [
        {
            "institute": "جامعة القاهرة",
            "degree": "بكالوريوس",
            "field_of_study": "هندسة البرمجيات",
            "start_date": "2016-09-01T00:00:00.000",
            "end_date": "2020-06-30T00:00:00.000",
            "description": "دراسة متخصصة في هندسة البرمجيات وتطوير التطبيقات."
        },
    ],
    "languages": ["العربية", "الإنجليزية"]
}

Example Output for English CV:
{
    "bio": "Software engineer with extensive experience in web and mobile application development.",
    "name": "Mohamed Ahmed",
    "email": "mohamed.ahmed@example.com",
    "contact_info": {"address": "Cairo, Egypt", "linkedin": "linkedin.com/in/mohamed-ahmed", "github": "github.com/mohamed-ahmed", "phone": "+201234567890", "whatsapp": "+201234567890"},
    "major": "Software Engineering",
    "skills": ["Web Development", "Mobile Applications", "Databases"],
    "experiences": [
        {
            "title": "Software Engineer",
            "company": "Tech Company",
            "start_date": "2020-01-01T00:00:00.000",
            "end_date": "2023-12-31T00:00:00.000",
            "location": "Cairo, Egypt",
            "description": "Developed web applications using React and Node.js."
        },
    ],
    "educations": [
        {
            "institute": "Cairo University",
            "degree": "Bachelor",
            "field_of_study": "Software Engineering",
            "start_date": "2016-09-01T00:00:00.000",
            "end_date": "2020-06-30T00:00:00.000",
            "description": "Specialized studies in software engineering and application development."
        },
    ],
    "languages": ["Arabic", "English"]
}
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
5. Job Description: Provide a detailed description of the job as mentioned in the text, in raw text without any bullet points.
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
    The 'ats_score' should be a float between 0.0 and 1.0.
    The score must follow these guidelines.
    For example:
    If a CV does not strictly meet the evaluation criteria, its score should be below 0.3.
    If a CV is rich in relevant content, its score should be above 0.4.

4. Suggestions:
   - Provide specific and actionable suggestions to improve the CV’s ATS-friendliness.
   - Each suggestion should correspond to one of the evaluation criteria mentioned above.
   - Ensure suggestions are clear, concise, and relevant to improving the ATS score.

5. Your response should be in a json format, don't add any additional text outside the json.

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
As an advanced matching system, please evaluate the compatibility between the candidate's experiences, skills, and education and the job's description, required skills, and responsibilities. Provide a match score as a float between 0.0 and 1.0, where 1.0 indicates a perfect match and 0.0 indicates no match at all.

Important Factors:
1. Relevant Skills: Evaluate how well the candidate's skills match the required skills for the job.
2. Years of Experience: Consider the candidate's years of experience in the relevant field compared to the job requirements.
3. Alignment with Job Description: Assess how closely the candidate's experiences align with the job description.
4. Education: Consider the candidate's education background and how well it aligns with the job requirements.
5. Job Responsibilities: Evaluate how well the candidate's past experiences and skills align with the responsibilities of the job.

Output Format:
- Return only a single float number as the match score.
- Do not provide any descriptive text or additional explanations.

Example:
A candidate who has all the required skills, significant years of relevant experience, a suitable education background, and experiences closely aligned with the job description and responsibilities might receive a score close to 1.0. Conversely, a candidate lacking these might receive a score close to 0.0.

Please provide the match score based on the above criteria.
"""
