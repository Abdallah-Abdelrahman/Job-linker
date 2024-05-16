"""Job Model"""
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from server.models.base_model import Base, BaseModel
from server.models.skill import job_skills


class Job(BaseModel, Base):
    """Job Class"""

    __tablename__ = "jobs"

    recruiter_id = Column(
            String(60),
            ForeignKey("recruiters.id"),
            nullable=False
            )
    major_id = Column(String(60), ForeignKey("majors.id"), nullable=False)
    job_title = Column(String(100), nullable=False)
    job_description = Column(Text, nullable=False)
    location = Column(String(128), nullable=True)
    exper_years = Column(String(128), nullable=True)
    salary = Column(Numeric(precision=10, scale=2, asdecimal=False))
    application_deadline = Column(DateTime, nullable=True)
    is_open = Column(Boolean, default=True)
    responsibilities = Column(JSON, nullable=True)

    # Relationship with Skill
    skills = relationship(
        "Skill",
        secondary=job_skills,
        back_populates="jobs",
    )

    # Relationship with Application
    applications = relationship(
        "Application", backref="job", cascade="all, delete-orphan"
    )

    @property
    def to_dict(self):
        """Return a dictionary reppresentation of Job"""
        dict_ = super().to_dict
        dict_["skills"] = [s.name for s in self.skills]
        dict_["major"] = self.major.name
        dict_["application_deadline"] = self.application_deadline
        dict_["is_open"] = self.is_open
        dict_["responsibilities"] = self.responsibilities
        return dict_

    def __repr__(self):
        """Return a string representation of the Job instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.job_title}"
