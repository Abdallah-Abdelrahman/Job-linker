"""Job Model"""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel
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
    exper_year = Column(String(128), nullable=True)

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

    @property
    def to_dict(self):
        """Return a dictionary representation of the Job instance"""
        job_dict = super().to_dict
        job_dict["job_title"] = self.job_title
        job_dict["job_description"] = self.job_description
        job_dict["exper_year"] = self.exper_year
        job_dict["skills"] = [skill.name for skill in self.skills]
        return job_dict
