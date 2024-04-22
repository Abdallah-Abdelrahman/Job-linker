"""User Class"""

from sqlalchemy import Column, Enum, String

from models.basemodel import Base, BaseModel


class User(Base, BaseModel):
    """User Model"""

    __tablename__ = "users"

    name = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum("candidate", "recruiter"), nullable=False)
    contact_info = Column(String(100))
    bio = Column(String(500))
    image_url = Column(String(200))

    def __repr__(self):
        """Return a string representation of the User instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.email}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the User instance"""
        user_dict = super().to_dict
        user_dict["email"] = self.email
        user_dict["role"] = self.role
        return user_dict
