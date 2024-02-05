from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from database import Base, configure_metadata

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class ConfigDataORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'config_dados'

    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)
    telefone = Column(String)
    phone_type = Column(Integer)
    endereco = Column(String)
    cep = Column(String)
    cnpj = Column(String)
    email = Column(String)
    whatsapp_message = Column(String)
    color = Column(String)