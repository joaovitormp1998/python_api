from pydantic import BaseModel
from typing import List
from .company import Company, CompanyResponse
from typing import Optional
from datetime import datetime


class ProductInvoice(BaseModel):
    categoria: str
    nome: str
    unidade_de_medida: str
    valor: float


class OrdemServico(BaseModel):
    company_id: Optional[int] = None
    user_id: Optional[int] = None
    status: str
    tipo_cliente: str
    cliente: Optional[str] = None
    contrato: Optional[str] = None
    pagamento: Optional[str] = None
    stripe_pagamento_id: Optional[str] = None
    informacoes_do_servico: Optional[str] = None
    imposto_percentual: Optional[float] = None
    desconto_percentual: Optional[float] = None
    produtos: Optional[List[ProductInvoice]] = None
    total: Optional[float] = None
    created_at:  Optional[datetime] = None
    validade: Optional[datetime] = None


class OrdemServicoCreate(BaseModel):
    company_id: Optional[int] = None
    user_id: Optional[int] = None
    status: str
    # products_ids : array


class OrdemServicoResponse(OrdemServico):
    id: int


class ProductInvoiceResponse(ProductInvoice):
    id: int


class OrdemServicoCreate(BaseModel):
    company_id: Optional[int] = None
    status: str
    products: List[ProductInvoice]
