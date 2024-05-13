"""Recruiter Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from server.models.base_model import Base, BaseModel


class Recruiter(BaseModel, Base):
    """Recruiter Model"""

    __tablename__ = "recruiters"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    user = relationship('User',
                        backref='recruiter',
                        uselist=False,
                        single_parent=True,
                        cascade='all, delete-orphan')
    # Relationship with Recruiter
    jobs = relationship(
            "Job",
            backref="recruiter",
            cascade="all, delete-orphan"
            )

    def __repr__(self):
        """Return a string representation of the Recruiter instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.company_name}"
