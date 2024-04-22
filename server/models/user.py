"""User Class"""

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel


class User(Base, BaseModel):
    """User Model"""

    __tablename__ = "users"
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum("candidate", "recruiter"), nullable=False)

    # Relationships
    profile = relationship("Profile", uselist=False, back_populates="user")
    candidate = relationship("Candidate", uselist=False, back_populates="user")
    recruiter = relationship("Recruiter", uselist=False, back_populates="user")

    def __init__(self, *args, **kwargs):
        """Initialize the User instance"""
        super().__init__(*args, **kwargs)

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
