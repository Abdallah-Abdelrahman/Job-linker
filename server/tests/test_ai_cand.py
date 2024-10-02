'''test ai'''
from os import getcwd, listdir
from server.models.candidate import Candidate
from server.models.major import Major
from server.models.skill import Skill
from server.models.user import User
from server.models.work_experience import WorkExperience
from server.models.language import Language
from server.models import storage
from server.services.ai import AIService
from server.prompts import CANDID_PROMPT


def create_candidate(cv=''):
    '''create new candidate
    Args:
        cv: path to resume file
    Returns:
        instance of newly created candiate
    '''
    # parse cv and generate dictionary
    cv_dict = AIService(pdf=f'{getcwd()}/server/cv/{cv}')\
        .to_dict(CANDID_PROMPT)

    # create user
    user_candid = User(
            email=cv_dict.get('email'),
            password='123123',
            role='candidate',
            name=cv_dict.get('name'))

    storage.new(user_candid)
    storage.save()

    # Create a Major
    queried_major = storage._DBStorage__session.query(Major)\
        .filter(Major.name.ilike(f'%{cv_dict.get("major")}%'))\
        .first()
    if queried_major:
        major = queried_major
    else:
        major = Major(name=cv_dict.get('major'))
    storage.new(major)
    storage.save()

    candidate = Candidate(user_id=user_candid.id, major_id=major.id)

    cand_skills = []
    # create bulk of skills
    for sk in cv_dict.get('skills'):
        filter_ = Skill.name.ilike(f'%{sk}%')
        queried = storage._DBStorage__session.query(Skill).filter(filter_).first()
        if queried:
            cand_skills.append(queried)
        else:
            cand_skills.append(Skill(name=sk))
    candidate.skills = cand_skills

    storage.new(candidate)
    storage.save()

    # Create a bulk of WorkExperience
    xps = [WorkExperience(candidate_id=candidate.id, **x)
           for x in cv_dict.get('experiences')]
    for xp in xps:
        storage.new(xp)
        storage.save()

    for l in cv_dict.get('languages'):
        queried_lang = storage._DBStorage__session.query(Language).filter(Language.name.ilike(f'%{l}%')).first()
        if queried_lang:
            candidate.languages.append(queried_lang)
        else:
            candidate.languages.append(Language(name=l))

    return candidate


if __name__ == '__main__':
    new_candid = create_candidate(cv='Abdallah.pdf')
    print(new_candid.to_dict)

    '''
    for f in listdir(f'{getcwd()}/server/cv'):
        try:
            new_candid = create_candidate(cv=f)
            print(new_candid.to_dict)
        except Exception as e:
            storage._DBStorage__session.rollback()
            print('-------->', e)
    '''
