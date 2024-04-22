from models.basemodel import Base, BaseModel
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()


class TestModel(Base, BaseModel):
    __tablename__ = "test_model"
    test_field = Column(String(50))


Base.metadata.create_all(engine)

test_instance = TestModel(test_field="Hello, world!")
session.add(test_instance)
session.commit()

queried_instance = session.query(TestModel).first()
print(queried_instance)
print()
print(queried_instance.id)
print(queried_instance.created_at)
print(queried_instance.updated_at)
print(queried_instance.test_field)
print(queried_instance.to_dict)
