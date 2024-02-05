from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func, Enum
from database import Base, configure_metadata

from sqlalchemy.orm import relationship

class DomainsORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String)
    tenant_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(String)
