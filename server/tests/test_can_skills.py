from models.basemodel import Base
from models.candidate import Candidate
from models.profile import Profile
from models.recruiter import Recruiter
from models.skill import Skill
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Create some skills
skills = ["Python", "SQL", "Java", "C++", "JavaScript"]
for skill_name in skills:
    skill = Skill(name=skill_name)
    session.add(skill)
session.commit()

# Create a candidate user
candidate_user = User(email="moh@123.com", password="123123", role="candidate")
session.add(candidate_user)
session.commit()

candidate_profile = Profile(
    name="Mohannad", contact_info="1234567890", user_id=candidate_user.id
)
session.add(candidate_profile)
session.commit()

candidate = Candidate(user_id=candidate_user.id, major="Computer Science")
session.add(candidate)
session.commit()

# Add skills to the candidate
candidate.skills = session.query(Skill).filter(Skill.name.in_(["Python", "SQL"])).all()
session.commit()

# Query the users, profiles, candidates, recruiters, and skills
queried_users = session.query(User).all()
queried_profiles = session.query(Profile).all()
queried_candidates = session.query(Candidate).all()
queried_recruiters = session.query(Recruiter).all()
queried_skills = session.query(Skill).all()

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

for skill in queried_skills:
    print(skill)
    print(skill.to_dict)
    print()
