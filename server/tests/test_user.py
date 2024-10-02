from models.base_model import Base
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

test_instance = User(email="moh@123.com", password="123123", role="candidate")
session.add(test_instance)
session.commit()

queried_instance = session.query(User).first()
print(queried_instance)
print()
print(queried_instance.id)
print(queried_instance.created_at)
print(queried_instance.updated_at)
print(queried_instance.email)
print(queried_instance.role)

print(queried_instance.to_dict)
