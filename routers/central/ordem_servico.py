from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timedelta

from models.central.ordem_servico import OrdemServico, OrdemServicoResponse, ProductInvoice, ProductInvoiceResponse
from database.central.product_invoice import OrdemServicoORM, ProductInvoiceORM, OrdemServicoProductInvoiceORM
from database.central.company import CompanyORM
from database.central.users import UserORM
from utils.jwt_token import has_authenticated, has_admin
import asyncio
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix='/api')


class Produto(BaseModel):
    id: int
    nome: str
    categoria: str
    valor: float
    unidade_de_medida: str
    quantity: int


class OS(BaseModel):
    categoria: str
    tipo_cliente: str
    user_id: Optional[int]
    company_id: Optional[int]
    status: str
    informacoes_do_servico: str
    contrato: str = "Pedente"
    pagamento: str = "Pedente"
    imposto_percentual: float
    desconto_percentual: float
    stripe_pagamento_id: Optional[str]
    total: float
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class FormSubmitted(BaseModel):
    ordem_servico: OS
    basketItens: List[Produto]


async def get_ordens_servico() -> List[dict]:
    ordens_servico = await OrdemServicoORM.find_many()

    async def fetch_additional_info(ordem_servico):
        cliente_pj = await CompanyORM.find_one(id=ordem_servico.company_id)
        cliente_fisico = await UserORM.find_one(id=ordem_servico.user_id)
        # Fetch the table linking products and service orders
        tabela_de_ligacao = await OrdemServicoProductInvoiceORM.find_many(ordem_servico_id=ordem_servico.id)

        # Fetch information about products related to the service order
        produtos = []
        subtotal = 0  # Initialize subtotal variable

        for ligacao in tabela_de_ligacao:
            produto = await ProductInvoiceORM.find_one(id=ligacao.product_invoice_id)
            if produto:
                subtotal += produto.valor  # Add the value of the product to the subtotal
                produtos.append({
                    "produto_id": ligacao.product_invoice_id,
                    "nome_produto": produto.nome,
                    "categoria": produto.categoria,
                    "nome": produto.nome,
                    "unidade_de_medida": produto.unidade_de_medida,
                    "valor": produto.valor,
                })
         # Calculate validade (created_at + 3 days)
        validade = ordem_servico.created_at + timedelta(days=3)
        return {
            "id": ordem_servico.id,
            "company_id": ordem_servico.company_id,
            "user_id": ordem_servico.user_id,
            "status": ordem_servico.status,
            "tipo_cliente":ordem_servico.tipo_cliente,
            "contrato": ordem_servico.contrato,
            "pagamento": ordem_servico.pagamento,
            "imposto_percentual":ordem_servico.imposto_percentual,
            "desconto_percentual":ordem_servico.desconto_percentual,
            "stripe_pagamento_id": ordem_servico.stripe_pagamento_id if ordem_servico.stripe_pagamento_id is not None else '',
            "cliente": cliente_pj.nome_fantasia if cliente_pj else cliente_fisico.name,
            "produtos": produtos,
            "created_at": ordem_servico.created_at,
            "total": subtotal,
            "validade": validade  # Include the calculated subtotal in the result
        }

    # Use asyncio.gather to parallelize database queries
    results = await asyncio.gather(*(fetch_additional_info(ordem_servico) for ordem_servico in ordens_servico))

    return results

async def get_ordem_servico(ordem_servico_id: int):
    ordem_servico = await OrdemServicoORM.find_one(id=ordem_servico_id)
    async def fetch_additional_info(ordem_servico):
        cliente_pj = await CompanyORM.find_one(id=ordem_servico.company_id)
        cliente_fisico = await UserORM.find_one(id=ordem_servico.user_id)
        tabela_de_ligacao = await OrdemServicoProductInvoiceORM.find_many(ordem_servico_id=ordem_servico.id)

        produtos = []
        subtotal = 0

        for ligacao in tabela_de_ligacao:
            produto = await ProductInvoiceORM.find_one(id=ligacao.product_invoice_id)
            if produto:
                subtotal += produto.valor
                produtos.append({
                    "produto_id": ligacao.product_invoice_id,
                    "nome_produto": produto.nome,
                    "categoria": produto.categoria,
                    "nome": produto.nome,
                    "unidade_de_medida": produto.unidade_de_medida,
                    "valor": produto.valor,
                })

        validade = ordem_servico.created_at + timedelta(days=3)
        return {
            "id": ordem_servico.id,
            "company_id": ordem_servico.company_id,
            "user_id": ordem_servico.user_id,
            "status": ordem_servico.status,
            "tipo_cliente": ordem_servico.tipo_cliente,
            "contrato": ordem_servico.contrato,
            "pagamento": ordem_servico.pagamento,
            "imposto_percentual": ordem_servico.imposto_percentual,
            "desconto_percentual": ordem_servico.desconto_percentual,
            "stripe_pagamento_id": ordem_servico.stripe_pagamento_id if ordem_servico.stripe_pagamento_id is not None else '',
            "cliente": cliente_pj.nome_fantasia if cliente_pj else cliente_fisico.name,
            "produtos": produtos,
            "created_at": ordem_servico.created_at,
            "total": subtotal,
            "validade": validade
        }

    # Use asyncio.gather to parallelize database queries
    results = await fetch_additional_info(ordem_servico)

    return results



@router.get('/ordens_servico', status_code=200, name='Lista ordens de serviço', response_model=List[OrdemServicoResponse], tags=['Ordens de Serviço'])
async def ordens_servico(user: dict = Depends(has_authenticated)):
    return await get_ordens_servico()


@router.get('/ordens_servico/{ordem_servico_id}', status_code=200, name='Obtém uma ordem de serviço', response_model=OrdemServicoResponse, tags=['Ordens de Serviço'])
async def ordem_servico(ordem_servico_id: int, user: dict = Depends(has_authenticated)):
    return await get_ordem_servico(ordem_servico_id)


@router.post('/ordens_servico', status_code=201, name='Cria uma ordem de serviço', tags=['Ordens de Serviço'])
async def ordem_servico_create(form_data: FormSubmitted, user: dict = Depends(has_authenticated)):
    try:
        # Create the main order of service
        ordem_servico_data = form_data.ordem_servico
        ordem_servico_instance = await OrdemServicoORM.create(**ordem_servico_data.dict())

        # Link existing product invoices to the order of service
        product_invoices = []

        for produto_data in form_data.basketItens:
            product_id = produto_data.id  # Assuming 'id' is the field for existing product ID
            quantity = produto_data.quantity

            # Create entries in ordem_servico_product_invoice based on the quantity
            for _ in range(quantity):
                await OrdemServicoProductInvoiceORM.create(ordem_servico_id=ordem_servico_instance.id, product_invoice_id=product_id)

                # Fetch product data from database
                product_invoice = await ProductInvoiceORM.find_one(id=product_id)
                product_invoices.append(ProductInvoiceResponse(**product_invoice.dict()))

        # Return the order of service along with the linked product invoices
        return OrdemServicoResponse(**ordem_servico_instance.dict())

    except HTTPException as e:
        print(f"HTTPException occurred: {e}")
        raise  # Re-raise the exception to allow FastAPI to handle it

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.put('/ordens_servico/{ordem_servico_id}', status_code=201, name='Edita uma ordem de serviço', response_model=List[OrdemServicoResponse], tags=['Ordens de Serviço'])
async def ordem_servico_edit(ordem_servico_id: int, params: OrdemServico, user: dict = Depends(has_authenticated)):
    await OrdemServicoORM.update(ordem_servico_id, **params.dict())
    return await get_ordens_servico()


@router.delete('/ordens_servico/{ordem_servico_id}', status_code=201, name='Exclui uma ordem de serviço', response_model=List[OrdemServicoResponse], tags=['Ordens de Serviço'])
async def ordem_servico_delete(ordem_servico_id: int, user: dict = Depends(has_authenticated)):
    await OrdemServicoORM.delete(id=ordem_servico_id)
    return await get_ordens_servico()


@router.post('/ordens_servico/{ordem_servico_id}/products', status_code=201, name='Adiciona produtos a uma ordem de serviço', response_model=List[ProductInvoiceResponse], tags=['Ordens de Serviço'])
async def add_products_to_ordem_servico(ordem_servico_id: int, products: List[ProductInvoice], user: dict = Depends(has_authenticated)):
    ordem_servico = await OrdemServicoORM.find_one(id=ordem_servico_id)

    if not ordem_servico:
        raise HTTPException(
            status_code=404, detail="Ordem de serviço não encontrada")

    product_invoices = []

    for product in products:
        product_invoice = await ProductInvoiceORM.create(**product.dict())
        await ordem_servico.products.append(product_invoice)
        product_invoices.append(
            ProductInvoiceResponse(**product_invoice.dict()))

    return product_invoices
