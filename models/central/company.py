from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    cargo_criador: str
    razao_social: str
    nome_fantasia: Optional[str]
    cnpj: str
    insc_estadual: str
    insc_municipal: str
    telefone: str
    email: str
    endereco: str
    numero: str
    complemento: str
    bairro: str
    cep: str
    cidade: str
    estado: str
    pais: str
    created_by: int

class CompanyUpdate(BaseModel):
    cargo_criador: str = None
    razao_social: str = None
    nome_fantasia: str = None
    cnpj: str = None
    insc_estadual: str = None
    insc_municipal: str = None
    telefone: str = None
    email: str = None
    endereco: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    cep: str = None
    cidade: str = None
    estado: str = None
    pais: str = None
    created_by: int = None
class CompanyResponse(Company):
    id: int
    dono:str