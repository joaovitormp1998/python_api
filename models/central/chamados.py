from pydantic import BaseModel


class Chamado(BaseModel):
    created_by: int
    descricao: str
    tipo: str
    status: str


class ChamadoResponse(Chamado):
    id: int
    cliente: str
