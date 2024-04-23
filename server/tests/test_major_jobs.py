from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base_model import Base
from models.candidate import Candidate
from models.job import Job
from models.major import Major
from models.recruiter import Recruiter
from models.skill import Skill
from models.user import User
from models.work_experience import WorkExperience

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Create a candidate user
candidate_user = User(
    email="moh@123.com", password="123123", role="candidate", name="Abdallah"
)
session.add(candidate_user)
session.commit()


# Create a Major
major = Major(name="Computer Science")
session.add(major)
session.commit()

# Create a Candidate
candidate = Candidate(user_id=candidate_user.id, major_id=major.id)
session.add(candidate)
session.commit()

# Create a WorkExperience
expers = WorkExperience(candidate_id=candidate.id,
                        title='Software tester', company='X', location='U.S')
session.add(expers)
session.commit()

# Create some skills
skills = [
    "Python",
    "SQL",
    "Java",
    "C++",
    "JavaScript",
    "React",
    "Angular",
    "Node.js",
    "HTML",
    "CSS",
]
for skill_name in skills:
    skill = Skill(name=skill_name)
    session.add(skill)
session.commit()

# Add skills to the candidate
candidate.skills = session.query(Skill).filter(Skill.name.in_(["Python", "SQL"])).all()
session.commit()


# Create a recruiter user
recruiter_user = User(
    email="jane@123.com", password="123123", role="recruiter", name="Mohannad"
)
session.add(recruiter_user)
session.commit()

recruiter = Recruiter(
    user_id=recruiter_user.id,
    company_name="Tech Corp",
    company_info="A leading tech company",
)
session.add(recruiter)
session.commit()

# Create a Job
job = Job(
    recruiter_id=recruiter_user.id,
    major_id=major.id,
    job_title="Software Engineer",
    job_description="Develop and maintain software applications",
    exper_years="2 Years",
)
session.add(job)
session.commit()

# Add skills to the job
job.skills = session.query(Skill).filter(Skill.name.in_(["C++", "Java"])).all()
session.commit()


# Create additional candidate users and profiles
candidate_user2 = User(
    email="ali@123.com", password="456456", role="candidate", name="Jason"
)
session.add(candidate_user2)
session.commit()

# Create additional majors
major2 = Major(name="Electrical Engineering")
session.add(major2)
session.commit()

# Add skills to the candidates
candidate2 = Candidate(user_id=candidate_user2.id, major_id=major2.id)
session.add(candidate2)
session.commit()

candidate2.skills = (
    session.query(Skill).filter(Skill.name.in_(["React", "Node.js"])).all()
)
session.commit()

# Create additional recruiter users and profiles
recruiter_user2 = User(
    email="emma@123.com", password="789789", role="recruiter", name="HolaHola"
)
session.add(recruiter_user2)
session.commit()

# Create additional recruiters and jobs
recruiter2 = Recruiter(
    user_id=recruiter_user2.id,
    company_name="InnoTech Solutions",
    company_info="An innovative tech startup",
)
session.add(recruiter2)
session.commit()

job2 = Job(
    recruiter_id=recruiter_user2.id,
    major_id=major.id,
    job_title="Frontend Developer",
    job_description="Design and develop user interfaces",
    exper_years="5 Years",
)
session.add(job2)
session.commit()

# Add skills to the job
job2.skills = (
    session.query(Skill).filter(Skill.name.in_(["React", "HTML", "CSS"])).all()
)
session.commit()

# Query the users, profiles, candidates, recruiters, majors, and jobs
queried_users = session.query(User).all()
queried_candidates = session.query(Candidate).all()
queried_recruiters = session.query(Recruiter).all()
queried_majors = session.query(Major).all()
queried_jobs = session.query(Job).all()
queried_skills = session.query(Skill).all()

# Print the queried data
for user in queried_users:
    print(user)
    print(user.to_dict)
    print()

for candidate in queried_candidates:
    print(candidate)
    print(candidate.to_dict)
    print()

for recruiter in queried_recruiters:
    print(recruiter)
    print(recruiter.to_dict)
    print()

for major in queried_majors:
    print(major)
    print(major.to_dict)
    print()

for job in queried_jobs:
    print(job)
    print(job.to_dict)
    print()

for skill in queried_skills:
    print(skill)
    print(skill.to_dict)
    print()
