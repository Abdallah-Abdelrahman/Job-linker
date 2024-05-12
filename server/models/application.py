"""Application Model"""

from sqlalchemy import Column, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from server.models.base_model import Base, BaseModel


class Application(BaseModel, Base):
    """Application Model"""

    __tablename__ = "applications"

    job_id = Column(String(60), ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(
            String(60),
            ForeignKey("candidates.id"),
            nullable=False
            )
    application_status = Column(
        Enum("applied", "shortlisted", "rejected", "hired"), default="applied"
    )
    match_score = Column(Float, nullable=True)

    # Relationship with Job
    job = relationship("Job",
                       back_populates="applications",
                       )

    # Relationship with Candidate
    candidate = relationship("Candidate",
                             back_populates="applications",
                             )
