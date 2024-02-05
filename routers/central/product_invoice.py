from fastapi import APIRouter, Depends, HTTPException

from models.central.product_invoice import ProductInvoice, ProductInvoiceResponse
from database.central.product_invoice import ProductInvoiceORM
from utils.jwt_token import has_authenticated, has_admin

from typing import List

router = APIRouter(prefix = '/api')

async def get_products_invoices():
    products_invoices = await ProductInvoiceORM.find_many()
    return [ProductInvoiceResponse(**p.dict()) for p in products_invoices]


@router.get('/products_invoices', status_code = 200, name = 'Pega planos', response_model = List[ProductInvoiceResponse], tags = ['Backoffice - Produtos -  Produtos Invoice'])
@router.get('/backoffice/products_invoices', status_code = 200, name = 'Produtos de Invoice', tags = ['Backoffice - Produtos -  Produtos Invoice'])
async def products_invoices(user: dict = Depends(has_authenticated)):
    return await get_products_invoices()


@router.post('/backoffice/products_invoices', status_code = 201, name = 'Cria um Produto de uma Invoice', response_model = List[ProductInvoiceResponse], tags = ['Backoffice - Produtos -  Produtos Invoice'])
async def plan_create(params: ProductInvoice, admin: dict = Depends(has_admin)):
    await ProductInvoiceORM.create(**params.dict())
    return await get_products_invoices()


@router.put('/backoffice/products_invoices/{product_invoice_id}', status_code = 201, name = 'Edita um Produto de uma Invoice', response_model = List[ProductInvoiceResponse], tags = ['Backoffice - Produtos -  Produtos Invoice'])
async def plan_create(product_invoice_id: int, params: ProductInvoice, admin: dict = Depends(has_admin)):
    await ProductInvoiceORM.update(product_invoice_id, **params.dict())
    return await get_products_invoices()


@router.delete('/backoffice/products_invoices/{product_invoice_id}', status_code = 201, name = 'Exclui um  Produto de uma Invoice', response_model = List[ProductInvoiceResponse], tags = ['Backoffice - Produtos -  Produtos Invoice'])
async def plan_create(product_invoice_id: int, admin: dict = Depends(has_admin)):
    await ProductInvoiceORM.delete(id = product_invoice_id)
    return await get_products_invoices()


@router.get('/backoffice/products_invoices/{product_invoice_id}', status_code = 200, name = 'Obtem um  Produto de uma Invoice', response_model = ProductInvoiceResponse, tags = ['Backoffice - Produtos -  Produtos Invoice'])
async def plan_create(product_invoice_id: int, admin: dict = Depends(has_admin)):
    product_invoice = await ProductInvoiceORM.find_one(id = product_invoice_id)
    return ProductInvoiceResponse(**product_invoice.dict())