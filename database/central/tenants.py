from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func
from database import Base, configure_metadata
from database.central.group import GroupORM

from sqlalchemy.orm import relationship

class TenantsORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer)
    partner_id = Column(Integer)
    administrator_id = Column(Integer)
    service_id = Column(Integer)
    finance_id = Column(Integer)
    plan = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    data = Column(JSON)
