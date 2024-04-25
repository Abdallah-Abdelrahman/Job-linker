"""Job Model"""
from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from server.models.base_model import BaseModel, Base
from server.models.skill import job_skills


class Job(BaseModel, Base):
    """Job Class"""

    __tablename__ = "jobs"

    recruiter_id = Column(
            String(60),
            ForeignKey("recruiters.user_id"),
            nullable=False
            )
    major_id = Column(String(60), ForeignKey("majors.id"), nullable=False)
    job_title = Column(String(100), nullable=False)
    job_description = Column(String(500), nullable=False)
    exper_years = Column(String(128), nullable=True)
    salary = Column(Numeric(precision=2, scale=2))

    # Relationship with Recruiter
    recruiter = relationship("Recruiter", back_populates="jobs")

    # Relationship with Major
    major = relationship("Major", back_populates="jobs")

    # Relationship with Skill
    skills = relationship(
        "Skill",
        secondary=job_skills,
        back_populates="jobs",
    )

    @property
    def to_dict(self):
        '''Return a dictionary reppresentation of Job'''
        dict_ = super().to_dict
        dict_["skills"] = [s.name for s in self.skills]
        return dict_

    def __repr__(self):
        """Return a string representation of the Job instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.job_title}"
