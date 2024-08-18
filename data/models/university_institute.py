import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from data.models.database import Base

"""
Class for save institute data 
"""


class UniversityInstitute(Base):
    #better name for tablename
    __tablename__ = 'institute_information'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    university_name = Column(Text, nullable=False)
