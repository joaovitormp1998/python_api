from sqlalchemy import Column, Integer, String, ForeignKey, func
from database import Base, configure_metadata

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class GroupORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    # Estabeleça um relacionamento com os usuários associados ao grupo
    users = relationship("UserORM", back_populates="group")
