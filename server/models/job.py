"""Job Model"""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from models.skill import job_skills


class Job(Base, BaseModel):
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

    def __repr__(self):
        """Return a string representation of the Job instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.job_title}"
