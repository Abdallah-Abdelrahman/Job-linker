from profile import Profile

from models.base_model import Base
from models.candidate import Candidate
from models.recruiter import Recruiter
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

candidate = Candidate(
    user_id=candidate_user.id, major="Computer Science", skills="Python, SQL"
)
session.add(candidate)
session.commit()


# Create another candidate user
candidate_user_1 = User(
    email="mohannad@123.com", password="123123123", role="candidate"
)
session.add(candidate_user_1)
session.commit()

candidate_profile_1 = Profile(
    name="Mohannad Babeker", contact_info="249-1234567890", user_id=candidate_user_1.id
)
session.add(candidate_profile_1)
session.commit()

candidate_1 = Candidate(
    user_id=candidate_user_1.id, major="Computer Science", skills="Python, SQL"
)
session.add(candidate_1)
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

# Query the users, profiles, candidates, and recruiters
queried_users = session.query(User).all()
queried_profiles = session.query(Profile).all()
queried_candidates = session.query(Candidate).all()
queried_recruiters = session.query(Recruiter).all()

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
