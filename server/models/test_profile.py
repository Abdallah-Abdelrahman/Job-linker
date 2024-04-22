from profile import Profile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from basemodel import Base
from user import User

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

test_user = User(email="moh@123.com", password="123123", role="candidate")
session.add(test_user)
session.commit()

test_profile = Profile(name="Mohannad", contact_info="1234567890", user_id=test_user.id)
session.add(test_profile)
session.commit()

queried_user = session.query(User).first()
queried_profile = session.query(Profile).first()

print(queried_user)
print()
print(queried_user.id)
print(queried_user.created_at)
print(queried_user.updated_at)
print(queried_user.email)
print(queried_user.role)
print(queried_user.to_dict)
print()
print(queried_profile)
print()
print(queried_profile.id)
print(queried_profile.created_at)
print(queried_profile.updated_at)
print(queried_profile.name)
print(queried_profile.contact_info)
print(queried_profile.to_dict)
