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
1. **Language Handling**:
   - Detect the language of the CV (Arabic or English).
   - Return the extracted information in the same language as the CV.
   - If the CV contains both Arabic and English, prioritize the dominant language.

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
As a professional applicant tracking system (ATS) evaluator, please analyze the following CV text and provide a detailed assessment. The analysis should include the following in JSON format:
{
    "ats_score": "<float: ATS friendliness score between 0.0 and 1.0>",
    "suggestions": ["<str: Suggestion 1>", "<str: Suggestion 2>", "..."]
}

Guidelines:
1. **Input Format**: The CV is provided in raw text extracted from a PDF. Avoid making suggestions about visual aspects like font style, size, or design.

2. **Evaluation Criteria**: Base your analysis on the following sections:

   - **Profile Summary/About Me**: Evaluate for clarity, conciseness, relevance to the job role, and presence of industry-specific keywords. Check if it provides a strong personal branding statement.

   - **Education**: Assess proper formatting, relevance to the desired job, inclusion of complete details such as degrees, institutions, majors, and dates. Prioritize recent and relevant educational achievements.

   - **Work Experience**: Analyze the use of action verbs, the presence of quantifiable achievements (e.g., increased sales by 30%), relevance to the target job, and proper formatting (e.g., job titles, companies, dates). Ensure chronological order and clarity of responsibilities.

   - **Skills**: Check for relevance to the job, proper categorization into hard skills (e.g., programming languages) and soft skills (e.g., leadership), and ensure that skills are clearly listed, ideally in a dedicated section.

   - **Languages**: Include analysis of languages spoken, specifying proficiency levels (e.g., native, fluent, intermediate). Consider relevance to the job requirements.

   - **Contact Information**: Confirm the presence and accuracy of contact details such as phone number, professional email address, LinkedIn profile, and other relevant links (e.g., personal website or portfolio). Verify that no unnecessary personal details are included (e.g., date of birth, photograph).

3. **Scoring**:
    - The 'ats_score' should be a float between 0.0 and 1.0.
    - The score must be based on the overall ATS compatibility and adherence to the evaluation criteria.
    - Provide lower scores (below 0.3) for CVs that do not meet the basic requirements (e.g., missing sections, lack of relevance, poor formatting).
    - Provide higher scores (above 0.7) for CVs that excel in relevance, clarity, completeness, and use of keywords.

4. **Suggestions**:
   - Provide specific and actionable suggestions for improving the CV’s ATS-friendliness.
   - Each suggestion should correspond to one of the evaluation criteria mentioned above.
   - Make sure suggestions are clear, concise, and prioritized based on the impact on ATS-friendliness. Suggest both additions and modifications as necessary.

5. **Response Format**: Ensure your response is in valid JSON format with no additional text outside the JSON object.

Example Response:
{
    "ats_score": 0.85,
    "suggestions": [
        "Enhance the profile summary by incorporating more relevant industry keywords.",
        "Add quantifiable achievements to each work experience entry to demonstrate impact.",
        "Categorize skills into technical and soft skills, and ensure they align with the job requirements."
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
