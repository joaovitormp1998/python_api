from routers.central.tenants import router
from fastapi import Depends, Query, Path,HTTPException
import asyncio

from httpx import AsyncClient

from database import tenancy_initialize, tenancy_end
from database.central.products import ProductsORM
from database.central.tenants import TenantsORM
from database.central.domains import DomainsORM
from database.tenant.students import StudentsORM
from database.tenant.profiles import ProfileORM
from database.central.users import UserORM
from datetime import datetime
from fastapi.routing import Request


from models.central.tenants import TenantCreate, TenantsResponse, SiteResponse
from utils.jwt_token import has_authenticated, has_admin

from dotenv import load_dotenv
from os import getenv

load_dotenv()

url = 'http://localhost/api/products' if getenv('DOCS_PATH') or getenv('REDOCS_PATH') else 'https://tutorcasts.app/api/products'

async def get_tenants(user_id: int):
    products = await ProductsORM.find_many(created_by = user_id)
    response = TenantsResponse()
    if not products: return response

    for product in products:
        tenant = await TenantsORM.find_one(id = product.tenant_id)
        if not tenant: continue

        domain = await DomainsORM.find_one(tenant_id = tenant.id)
        if not domain: continue

        tenancy_initialize(tenant.data['tenancy_db_name'])
        students = await StudentsORM.find_many()
        response.students += len(students)

        site = SiteResponse(
            id = tenant.id,
            name = product.name,
            domain = domain.domain,
            status = domain.status,
            icon = product.photo,
            type = product.type,
            students = len(students),
        )
        response.sites.append(site)
        tenancy_end()

    return response


@router.get('/tenants', status_code = 200, name = 'Minhas instancias', response_model = TenantsResponse, tags = ['Tenants'])
async def tenants(user: dict = Depends(has_authenticated)):
    return await get_tenants(user.id)
    

@router.post('/tenants', status_code = 201, name = 'Criar uma instancia', response_model = TenantsResponse, tags = ['Tenants'])
async def tenant_create(params: TenantCreate, user: dict = Depends(has_authenticated)):
    data = params.dict()
    data['type_product'] = 'tenant'

    async with AsyncClient() as client:
        response = await client.post(f'{url}/{user.id}', data = data, timeout = 600)
        print(response)

    return await get_tenants(user.id)

@router.patch('/tenants/{tenant_id}', status_code=200, name='Muda status de uma instancia', tags=['Tenants'])
async def tenant_status(
    tenant_id: str,
    status:str = Query(..., title="ID do Novo Dono",
                                description="ID do Novo Dono"),
    user: dict = Depends(has_authenticated)
):

    domain = await DomainsORM.find_one(tenant_id=tenant_id)
    current_timestamp = datetime.utcnow()

    if domain:
        # Certifique-se de validar se o status é um valor válido antes de atualizar o banco de dados
        if status in ['activated', 'deactivating', 'deactivated']:
            await DomainsORM.update(domain.id, status=status, updated_at=current_timestamp)
            return {'Domain': domain}
        else:
            raise HTTPException(status_code=400, detail='Status inválido. Deve ser "activated", "deactivating" ou "deactivated".')
    else:
        raise HTTPException(status_code=404, detail='Produto não encontrado')

    return domain




async def get_tenants_backoffice(products):
    tenants = []
    tasks = []

    for product in products:
        tasks.append(process_product(product, tenants))

    await asyncio.gather(*tasks)

    return tenants

async def process_product(product, tenants):
    try:
        tenant = await TenantsORM.find_one(id=product.tenant_id)
        if not tenant:
            return

        domain = await DomainsORM.find_one(tenant_id=product.tenant_id)
        if not domain:
            return

        owner, partner, administrator, service, finance = await asyncio.gather(
            UserORM.find_one(id=product.created_by),
            UserORM.find_one(id=tenant.partner_id),
            UserORM.find_one(id=tenant.administrator_id),
            UserORM.find_one(id=tenant.service_id),
            UserORM.find_one(id=tenant.finance_id)
        )

        data = {
            'id': product.tenant_id,
            'name': product.name,
            'domain': domain.domain,
            'created_at': tenant.created_at,
            'active': domain.status,
            'owner': owner.name if owner else None,
            'partner': partner.name if partner else None,
            'administrator': administrator.name if administrator else None,
            'service': service.name if service else None,
            'finance': finance.name if finance else None
        }

        tenants.append(data)
    except Exception as e:
        # Tratar exceções conforme necessário
        print(f"Erro ao processar produto {product}: {e}")

@router.get('/backoffice/tenants', status_code = 200, name = 'Tenants', tags = ['Backoffice'])
async def tenants_backoffice(sudo: dict = Depends(has_admin)):
    products = await ProductsORM.find_many(type = 'tenant')
    return await get_tenants_backoffice(products)
# @router.get('/backoffice/tenants/{tenant_id}/management/general', status_code = 200, name = 'Tenants', tags = ['Backoffice'])
# async def tenants_backoffice(sudo: dict = Depends(has_admin)):
#     products = await ProductsORM.find_many(type = 'tenant')
#     return await get_tenants_backoffice(products)
