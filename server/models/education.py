"""Education model for the candidate"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text

from server.models.base_model import Base, BaseModel


class Education(BaseModel, Base):
    """Education Model"""

    __tablename__ = "educations"

    candidate_id = Column(
            String(60),
            ForeignKey("candidates.id"),
            nullable=False
            )
    institute = Column(String(128), nullable=True)
    degree = Column(String(128), nullable=True)
    field_of_study = Column(String(128), nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow())
    end_date = Column(DateTime, default=datetime.utcnow())
    description = Column(Text)

    def __repr__(self):
        """Return a string representation of the Education instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.institute}"
