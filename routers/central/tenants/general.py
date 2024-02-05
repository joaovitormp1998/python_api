from routers.central.tenants import router
from fastapi import Depends, HTTPException

from database import tenancy_initialize, tenancy_end
from database.central.products import ProductsORM
from database.central.tenants import TenantsORM
from database.central.domains import DomainsORM
from database.tenant.students import StudentsORM
from database.tenant.config_data import ConfigDataORM
from database.tenant.configs import ConfigsORM
from models.central.tenants import TenantGeneral, TenantGeneralResponse
from utils.jwt_token import has_authenticated


@router.get('/tenants/{tenant_id}/management/general', status_code = 200, name = 'Obtem informações gerais de uma instancia', response_model = TenantGeneralResponse, tags = ['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/general', status_code = 200, name = 'Obtem informações gerais de uma instancia', response_model = TenantGeneralResponse, tags = ['Backoffice'])
async def tenant_general(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id = tenant_id, created_by = user.id)
    product = await ProductsORM.find_one(tenant_id = tenant_id)
    if not product: raise HTTPException(status_code = 404, detail = 'Produto não  Encontrado')
    
    tenant = await TenantsORM.find_one(id = product.tenant_id)
    if not tenant: raise HTTPException(status_code = 404, detail = 'Tenant not found')
    domain = await DomainsORM.find_one(tenant_id = tenant.id)

    tenancy_initialize(tenant.data['tenancy_db_name'])
    config_data = await ConfigDataORM.find_one()
    config = await ConfigsORM.find_or_new(nome = 'company.attendance')
    students = await StudentsORM.find_many()

    response = TenantGeneralResponse(
        tenant = {
            'name': config_data.nome or "",
            'domain': domain.domain or "",
            'users': len(students) or 0,
            'status': domain.status or ""
        },
        
        domain =  domain.domain or "",
        name = config_data.nome or "",
        phone =  config_data.telefone or "",
        is_whatsApp =  config_data.phone_type == 1,
        whatsapp_message =  config_data.whatsapp_message or "",
        address =  config_data.endereco or "",
        zipcode =  config_data.cep or "",
        cnpj =  config_data.cnpj or "",
        email =  config_data.email or "",
        service =  config.valor or ""
    )
    tenancy_end()

    return response


@router.put('/tenants/{tenant_id}/management/general', status_code = 201, name = 'Edita informações gerais de uma instancia', response_model = TenantGeneralResponse, tags = ['Tenants'])
# @router.put('/backoffice/tenants/{tenant_id}/management/general', status_code = 201, name = 'Edita informações gerais de uma instancia', response_model = TenantGeneralResponse, tags = ['Backoffice'])
async def tenant_general_edit(params: TenantGeneral, tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id = tenant_id, created_by = user.id)
    product = await ProductsORM.find_one(tenant_id = tenant_id)
    if not product: raise HTTPException(status_code = 404, detail = 'Product not found')
    
    tenant = await TenantsORM.find_one(id = product.tenant_id)
    if not tenant: raise HTTPException(status_code = 404, detail = 'Tenant not found')
    domain = await DomainsORM.find_one(tenant_id = tenant.id)
     
    tenancy_initialize(tenant.data['tenancy_db_name'])
    config_data = await ConfigDataORM.find_one()
    config_data = await ConfigDataORM.update(config_data.id, 
        nome = params.name or "",
        telefone = params.phone or "",
        phone_type = params.is_whatsApp or 1,
        endereco = params.address or "",
        cep = params.zipcode or "",
        cnpj = params.cnpj or "",
        email = params.email or "",
        whatsapp_message = params.whatsapp_message or ""
    )

    config = await ConfigsORM.find_or_new(nome = 'company.attendance')
    await ConfigsORM.update(config.id, valor = params.service)
    students = await StudentsORM.find_many()
    print("Antes da atualização do domínio")
    print('Domain',params.domain)
    await DomainsORM.update(domain.id, domain=params.domain)
    print("Depois da atualização do domínio")

    response = TenantGeneralResponse(
        tenant = {
            'name': config_data.nome or "",
            'domain': domain.domain or "",
            'users': len(students) or 0,
            'status': domain.status or ""
        }, **params.dict()
    )
    tenancy_end()

    return response
