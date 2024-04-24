"""Languages Model"""
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel

# Association table for Language_Skill m:m relationship
candidate_languages = Table(
    "candidate_languages",
    Base.metadata,
    Column("candidate_id", String(60),
           ForeignKey("candidates.user_id"), primary_key=True),
    Column("lang_id", String(60),
           ForeignKey("languages.id"), primary_key=True),
)


class Language(Base, BaseModel):
    """Language Class"""

    __tablename__ = "languages"

    name = Column(String(100), nullable=False)

    # Relationship with Candidate and associative table
    candidates = relationship(
        "Candidate",
        secondary=candidate_languages,
        back_populates="languages",
    )

    def __repr__(self):
        """Return a string representation of the Language instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"
