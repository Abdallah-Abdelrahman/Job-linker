"""WorkExperience Class"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import backref, relationship

from server.models.base_model import Base, BaseModel


class WorkExperience(BaseModel, Base):
    """WorkExperience Model

    Attrs:
        __tablename__: table name
        candidate_id: foreign key references `Candidate`
        company: company name
        title: title of work experience
        location: location of job
        start_date: start date of the job
        end_date: end date of the job
        description: thorough despcriont of job
        candidate: realtional field
    """

    __tablename__ = "work_experiences"

    candidate_id = Column(
            String(60),
            ForeignKey("candidates.id"),
            nullable=False
            )
    title = Column(String(128), nullable=False)
    company = Column(String(128), nullable=False)
    location = Column(String(128))
    start_date = Column(DateTime, default=datetime.utcnow())
    end_date = Column(DateTime, default=datetime.utcnow())
    description = Column(Text)

    candidate = relationship(
        "Candidate", backref=backref("experiences", cascade="all, delete")
    )

    def __repr__(self):
        """Return a string representation of the WorkExperience instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.title}"
