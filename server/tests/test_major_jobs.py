'''test'''
from models.candidate import Candidate
from models.job import Job
from models.major import Major
from models.recruiter import Recruiter
from models.skill import Skill
from models.user import User
from models.work_experience import WorkExperience
from models.language import Language
from models import storage

# Create some skills
SKILLS = [
    'Python',
    'SQL',
    'Java',
    'C++',
    'JavaScript',
    'React',
    'Angular',
    'Node.js',
    'HTML',
    'CSS',
]

# Create a candidate user
candidate_user = User(
        email='moh@123.com',
        password='123123',
        role='candidate',
        name='Abdallah')

storage.new(candidate_user)
storage.save()


# Create a Major
major = Major(name='Computer Science')
storage.new(major)
storage.save()

# Create bulk of skills
skills = [Skill(name=s) for s in SKILLS]

for skill in skills:
    storage.new(skill)
    storage.save()

# Create a Candidate
candidate = Candidate(
        user_id=candidate_user.id,
        major_id=major.id,
        languages=[Language(name=lang) for lang in ['english', 'arabic']],
        skills=skills[:3]
)

storage.new(candidate)
storage.save()

# Create a WorkExperience
expers = WorkExperience(
        candidate_id=candidate.id,
        title='Software tester',
        company='X',
        location='U.S')

storage.new(expers)
storage.save()

# Create a recruiter user
recruiter_user = User(
        email='jane@123.com',
        password='123123',
        role='recruiter',
        name='Mohannad')

storage.new(recruiter_user)
storage.save()

recruiter = Recruiter(
        user_id=recruiter_user.id,
        company_name='Tech Corp',
        company_info='A leading tech company',
)
storage.new(recruiter)
storage.save()

# Create a Job
job = Job(
    recruiter_id=recruiter_user.id,
    major_id=major.id,
    job_title="Software Engineer",
    job_description="Develop and maintain software applications",
    exper_years="2 Years",
    salary=2000.500
)
storage.new(job)
storage.save()


# Create newitional candidate users and profiles
candidate_user2 = User(
        email='ali@123.com',
        password='456456',
        role='candidate',
        name='Jason'
)
storage.new(candidate_user2)
storage.save()

# Create newitional majors
major2 = Major(name='Electrical Engineering')
storage.new(major2)
storage.save()

# new skills to the candidates
candidate2 = Candidate(
        user_id=candidate_user2.id,
        major_id=major2.id,
        skills=skills[4:9]
)
storage.new(candidate2)
storage.save()

# Create newitional recruiter users and profiles
recruiter_user2 = User(
        email='emma@123.com',
        password='789789',
        role='recruiter',
        name='HolaHola'
)
storage.new(recruiter_user2)
storage.save()

# Create newitional recruiters and jobs
recruiter2 = Recruiter(
        user_id=recruiter_user2.id,
        company_name='InnoTech Solutions',
        company_info='An innovative tech startup',
)
storage.new(recruiter2)
storage.save()

job2 = Job(
    recruiter_id=recruiter_user2.id,
    major_id=major.id,
    job_title='Frontend Developer',
    job_description='Design and develop user interfaces',
    exper_years='5 Years',
    skills=skills[5:10],
    salary=5000.678999
)
storage.new(job2)
storage.save()

# Query the users, profiles, candidates, recruiters, majors, and jobs
queried_users = storage.all(User)
queried_candidates = storage.all(Candidate)
queried_recruiters = storage.all(Recruiter)
queried_majors = storage.all(Major)
queried_jobs = storage.all(Job)
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

for recruiter in queried_recruiters.values():
    print(recruiter)
    print(recruiter.to_dict)
    print()

for major in queried_majors.values():
    print(major)
    print(major.to_dict)
    print()

for job in queried_jobs.values():
    print(job)
    print(job.to_dict)
    print()

for skill in queried_skills.values():
    print(skill)
    print(skill.to_dict)
    print()
