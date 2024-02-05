from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from database import Base, configure_metadata

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class StylesORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'estilos'

    id = Column(Integer, primary_key = True, index = True)
    logo = Column(String)
    icon = Column(String)
    botoes = Column(String)
    fonte_botoes = Column(String)
    barra_superior = Column(String)
    fonte_barra_superior = Column(String)
    barra_modais = Column(String)
    barra_menu = Column(String)
    fonte_menu = Column(String)
    barra_rodape = Column(String)
    fonte_barra_rodape = Column(String)
    background_logo = Column(String)
    facebook_widget = Column(String)
    professores_bg = Column(String)
    depoimentos_bg = Column(String)
