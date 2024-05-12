"""Recruiter Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from server.models.base_model import Base, BaseModel


class Recruiter(BaseModel, Base):
    """Recruiter Model"""

    __tablename__ = "recruiters"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    company_info = Column(String(500))

    # Relationship with User & Job
    user = relationship(
        "User",
        backref=backref("recruiter",
                        uselist=False,
                        cascade="all, delete-orphan"
                        )
    )

    def __repr__(self):
        """Return a string representation of the Recruiter instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.company_name}"
