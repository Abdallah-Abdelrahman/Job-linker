"""Recruiter Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from basemodel import Base, BaseModel


class Recruiter(Base, BaseModel):
    """Recruiter Model"""

    __tablename__ = "recruiters"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    company_info = Column(String(500))

    # Relationship with User
    user = relationship("User", back_populates="recruiter")

    def __repr__(self):
        """Return a string representation of the Recruiter instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.company_name}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Recruiter instance"""
        recruiter_dict = super().to_dict
        recruiter_dict["company_name"] = self.company_name
        recruiter_dict["company_info"] = self.company_info
        return recruiter_dict
