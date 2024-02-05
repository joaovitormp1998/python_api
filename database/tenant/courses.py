from sqlalchemy import Column, Integer, String,Float,Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship
from database import Base, configure_metadata
from models.central.user import UserSignUp

class CoursesORM(Base):
    metadata = configure_metadata()
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True)
    num_turma = Column(String)
    cod_disciplina = Column(String)
    nome = Column(String)
    turma_id = Column(Integer)  # Adicione o tipo de dado apropriado
    professor_id = Column(Integer)  # Adicione o tipo de dado apropriado
    tipo = Column(String)
    status = Column(String)
    objetivo = Column(String)
    video_demonstrativo = Column(String)
    corpo_docente = Column(String)
    pergunta_professor = Column(String)
    duracao_curso = Column(String)
    valor = Column(Float)  # Adicione o tipo de dado apropriado
    desconto_promocao = Column(Float)  # Adicione o tipo de dado apropriado
    desconto_boleto = Column(Float)  # Adicione o tipo de dado apropriado
    valor_promocional = Column(Float)  # Adicione o tipo de dado apropriado
    data_inicio_promocional = Column(DateTime)
    data_termino_promocional = Column(DateTime)
    data_despublicacao = Column(DateTime)
    data_expiracao_matriculas = Column(DateTime)
    duracao = Column(Integer)  # Adicione o tipo de dado apropriado
    justificativa = Column(String)
    publico_alvo = Column(String)
    cronograma = Column(String)
    regras_gerais = Column(String)
    gravacao_aulas = Column(String)
    vendavel = Column(String)
    matriculas_ilimitadas = Column(Boolean)  # Adicione o tipo de dado apropriado
    limite_alunos = Column(Integer)  # Adicione o tipo de dado apropriado
    invite_token = Column(String)
    data_criacao = Column(DateTime)
    data_edicao = Column(DateTime)
    valor_parcela = Column(Float)  # Adicione o tipo de dado apropriado
    explicacao_promocao = Column(String)
    imagem_curso = Column(String)
    banner_curso = Column(String)
    descricao_curso = Column(String)
    classificacao = Column(Float)  # Adicione o tipo de dado apropriado
    tcc = Column(String)
    perguntas = Column(String)
    redirecionar = Column(String)
    desabilita_boleto = Column(String)
    # Continue adicionando os campos restantes conforme necessário

    atualizado_em = Column(DateTime)
    atualizado_por = Column(String)
    nota_aprovacao = Column(Float)  # Adicione o tipo de dado apropriado
    participation_cert_enable = Column(Boolean)  # Adicione o tipo de dado apropriado
    participation_cert_text = Column(String)
    participation_cert_image = Column(String)
    participation_cert_attendance = Column(Float)  # Adicione o tipo de dado apropriado
    participation_cert_margin_top = Column(Float)  # Adicione o tipo de dado apropriado
    participation_cert_margin_bottom = Column(Float)  # Adicione o tipo de dado apropriado
    participation_cert_margin_left = Column(Float)  # Adicione o tipo de dado apropriado
    participation_cert_margin_right = Column(Float)  # Adicione o tipo de dado apropriado
    price_visible_enable = Column(Boolean)
    def __repr__(self):
        return f"<CoursesORM(id={self.id}, nome={self.nome}, price_visible_enable={self.price_visible_enable}, tipo={self.tipo}, status={self.status})>"
