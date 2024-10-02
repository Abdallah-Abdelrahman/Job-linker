'''test ai'''
from os import getcwd
from server.services.ai import AIService
from server.prompts import JOB_PROMPT
from server.models import storage
from server.models.candidate import Candidate
from server.models.major import Major
from server.models.job import Job
from server.models.recruiter import Recruiter
from server.models.user import User


def create_job(desc=''):
    '''Transform job description into a model
    Args:
        desc(str): text of job description
    Returns:
        isntance of job model
    '''
    pdf = f'{getcwd()}/server/jobs/'
    ai = AIService(pdf=pdf+desc)
    recruiter = User(
            name='someone',
            email='a@b.com',
            role='recruiter',
            recruiter=Recruiter(company_name='pta'))
    # parse job and generate dictionary
    dict_ = ai.to_dict(JOB_PROMPT)
    major = storage._DBStorage__session.query(Major)\
        .filter(Major.name.ilike('computer science')).first()
    job = Job(major_id=major.id, recruiter_id=recruiter.id, **dict_)
    print(dict_)
    return job


def short_list(pdf=''):
    '''Short list the candidates base on job description'''
    candids = [c.to_dict for c in storage.all(Candidate).values()]
    ai = AIService()

    if not candids:
        print('No candidates provided')
        return
    txt = f'''from this {candids} return candidates from most fit to job description to lowest:
         your response should be in this form:
         [{{name: str, id: str, user_id: str }}]

         Ranking creiteria:
         - relevant experience.
         - years of experience.
        '''
    print(ai.prompt(txt, input_txt=ai.parse_pdf(pdf=f'{getcwd()}/server/jobs/{pdf}')))

if __name__ == '__main__':
    short_list(pdf='job_desc_front_engineer.pdf')
