from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from database import Base, configure_metadata
from database.central.group import GroupORM

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class UserORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True)
    name = Column(String)
    password = Column(String)
    last_name = Column(String)
    phone = Column(String)
    photo = Column(String)
    document = Column(String)
    remember_token = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, onupdate = func.now())
    email_verified_at = Column(DateTime)

    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("GroupORM")
    
    company = relationship('CompanyORM', back_populates='users')
