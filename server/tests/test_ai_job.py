'''test ai'''
from os import getcwd
from server.services.ai import AIService
from server.prompts import JOB_PROMPT
from server.models import storage
from server.models.candidate import Candidate


def create_job(desc=''):
    '''Transform job description into a model
    Args:
        desc(str): text of job description
    Returns:
        isntance of job model
    '''
    # parse cv and generate dictionary
    ai = AIService(pdf=f'{getcwd()}/server/jobs/{desc}')
    dict_ = ai.to_dict(JOB_PROMPT)
    # pdf_txt = ai.parse_pdf()
    filter_ = f'%{dict_.get("major")}%'
    candids = storage._DBStorage__session.query(Candidate)\
        .filter(Candidate.major.name.ilike(filter_)).all()
    print(candids)


create_job(desc='job_desc_front_engineer.pdf')
