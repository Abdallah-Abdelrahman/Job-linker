from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.basemodel import Base
from models.candidate import Candidate
from models.job import Job
from models.major import Major
from models.profile import Profile
from models.recruiter import Recruiter
from models.skill import Skill
from models.user import User

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Create a candidate user
candidate_user = User(email="moh@123.com", password="123123", role="candidate")
session.add(candidate_user)
session.commit()

candidate_profile = Profile(
    name="Mohannad", contact_info="1234567890", user_id=candidate_user.id
)
session.add(candidate_profile)
session.commit()

# Create a Major
major = Major(name="Computer Science")
session.add(major)
session.commit()

candidate = Candidate(user_id=candidate_user.id, major_id=major.id)
session.add(candidate)
session.commit()

# Create a recruiter user
recruiter_user = User(email="jane@123.com", password="123123", role="recruiter")
session.add(recruiter_user)
session.commit()

recruiter_profile = Profile(
    name="Abdallah", contact_info="0987654321", user_id=recruiter_user.id
)
session.add(recruiter_profile)
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
    experience_start=datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
    experience_end=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
)
session.add(job)
session.commit()

# Query the users, profiles, candidates, recruiters, majors, and jobs
queried_users = session.query(User).all()
queried_profiles = session.query(Profile).all()
queried_candidates = session.query(Candidate).all()
queried_recruiters = session.query(Recruiter).all()
queried_majors = session.query(Major).all()
queried_jobs = session.query(Job).all()

# Print the queried data
for user in queried_users:
    print(user)
    print(user.to_dict)
    print()

for profile in queried_profiles:
    print(profile)
    print(profile.to_dict)
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
