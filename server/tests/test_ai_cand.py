'''test ai'''
from os import getcwd
from server.models.candidate import Candidate
from server.models.major import Major
from server.models.skill import Skill
from server.models.user import User
from server.models.work_experience import WorkExperience
from server.models.language import Language
from server.models import storage
from server.services.ai import AIService
from server.prompts import CANDID_PROMPT

# parse cv and generate dictionary
cv_dict = AIService(cv=f'{getcwd()}/server/cv/moe.pdf').to_dict(CANDID_PROMPT)

print(type(cv_dict))

# create user
user_candid = User(
        email=cv_dict.get('email'),
        password='123123',
        role='candidate',
        name=cv_dict.get('name'))

storage.new(user_candid)
storage.save()

# create bulk of skills
skills = [Skill(name=s) for s in cv_dict.get('skills')]
for skill in skills:
    storage.new(skill)
    storage.save()

# Create a Major
major = Major(name=cv_dict.get('major'))
storage.new(major)
storage.save()

# Create a Candidate
candidate = Candidate(
        user_id=user_candid.id,
        major_id=major.id,
        languages=[Language(name=lang) for lang in cv_dict.get('languages')],
        skills=skills
)
storage.new(candidate)
storage.save()

# Create a bulk of WorkExperience
xps = [WorkExperience(candidate_id=candidate.id, **x)
       for x in cv_dict.get('experiences')]
for xp in xps:
    storage.new(xp)
    storage.save()

# Query the users, profiles, candidates, recruiters, majors, and jobs
queried_users = storage.all(User)
queried_candidates = storage.all(Candidate)
queried_majors = storage.all(Major)
queried_skills = storage.all(Skill)

# Print the queried data
for user in queried_users.values():
    print(user)
    print(user.to_dict)
    print()

for candidate in queried_candidates.values():
    print(candidate)
    print(candidate.to_dict)
    print()

for major in queried_majors.values():
    print(major)
    print(major.to_dict)
    print()

for skill in queried_skills.values():
    print(skill)
    print(skill.to_dict)
    print()
