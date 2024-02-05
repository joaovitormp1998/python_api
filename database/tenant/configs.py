from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from database import Base, configure_metadata

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class ConfigsORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'configs'

    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)
    valor = Column(String)
    descricao = Column(String)