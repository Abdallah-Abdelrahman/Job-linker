'''test ai'''
from os import getcwd
from server.services.ai import AIService
from server.prompts import JOB_PROMPT

# parse cv and generate dictionary
cv_dict = AIService(
        cv=f'{getcwd()}/server/jobs/job_desc_front_engineer.pdf'
        ).to_dict(JOB_PROMPT)

print(type(cv_dict))
