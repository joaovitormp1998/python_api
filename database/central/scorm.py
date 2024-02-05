from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from database import Base, configure_metadata

from sqlalchemy.orm import relationship

class ScormORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'scorm'

    id = Column(Integer, primary_key = True, index = True)
    tenant_id = Column(String)
    s3_key = Column(String, unique = True)