from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from database import Base, configure_metadata

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class StudentsORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'alunos'

    class EmailMktEnum(Enum):
        YES = 'Sim'
        NO = 'Não'

    class SexEnum(Enum):
        MALE = 'Masculino'
        FEMALE = 'Feminino'

    class ApprovedConventionEnum(Enum):
        PENDING = 'Pendente'
        APPROVED = 'Aprovado'
        REFUSED = 'Recusado'

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer)
    # user_id = Column(Integer, ForeignKey('groups.id'))
    # user = relationship("GroupORM")
    nome = Column(String)
    email = Column(String)
    cpf = Column(String)
    rg = Column(String)
    rg_emissor = Column(String)
    data_nascimento = Column(DateTime)
    logradouro = Column(String)
    numero = Column(Integer)
    complemento = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(Integer)
    telefone1 = Column(Integer)
    telefone2 = Column(Integer)
    aceitarEmailMkt = Column(String)
    # aceitarEmailMkt = Column(EmailMktEnum, default = EmailMktEnum.NO)
    data_atualizacao = Column(DateTime)
    data_registro = Column(DateTime)
    sexo = Column(String)
    # sexo = Column(SexEnum)
    status_cadastro = Column(Integer)
    avatar = Column(String)
    foto_perfil = Column(String)
    convenio_id = Column(Integer)
    # convenio_id = Column(Integer, ForeignKey('groups.id'))
    # convenio = relationship("GroupORM")
    convenio_aprovado = Column(String)
    # convenio_aprovado = Column(ApprovedConventionEnum)
    confirmed_email = Column(Integer)
    confirmed_cellphone_at = Column(DateTime)
    force_update_card = Column(Integer)
    lti_id = Column(Integer)
    profissao_id = Column(Integer)
    # profissao_id = Column(Integer, ForeignKey('groups.id'))
    # profissao = relationship("GroupORM")
    registro_profissional = Column(String)
