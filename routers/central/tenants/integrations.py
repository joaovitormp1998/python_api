from routers.central.tenants import router
from fastapi import Depends, HTTPException

from database import tenancy_initialize, tenancy_end
from database.central.products import ProductsORM
from database.central.tenants import TenantsORM
from database.tenant.config_data import ConfigDataORM
from database.tenant.configs import ConfigsORM
from database.tenant.styles import StylesORM
from models.central.tenants import TenantIntegrations, TenantIntegrationsResponse
from utils.jwt_token import has_authenticated


@router.get('/tenants/{tenant_id}/management/integrations', status_code = 200, name = 'Obtem as integrações de uma instancia', response_model = TenantIntegrationsResponse, tags = ['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/integrations', status_code = 200, name = 'Obtem as integrações de uma instancia', response_model = TenantIntegrationsResponse, tags = ['Backoffice'])
async def tenant_integrations(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id = tenant_id, created_by = user.id)
    product = await ProductsORM.find_one(tenant_id = tenant_id)
    if not product: raise HTTPException(status_code = 404, detail = 'Product not found')
    
    tenant = await TenantsORM.find_one(id = product.tenant_id)
    if not tenant: raise HTTPException(status_code = 404, detail = 'Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])
    config_data = await ConfigDataORM.find_one();

    google_analytics_id = await ConfigsORM.find_or_new(nome = 'google.analytics_id')
    google_gtm_id = await ConfigsORM.find_or_new(nome = 'google.gtm_id')
    facebook_app_id = await ConfigsORM.find_or_new(nome = 'facebook.app_id')
    facebook_app_secret = await ConfigsORM.find_or_new(nome = 'facebook.app_secret')
    affiliates_email = await ConfigsORM.find_or_new(nome = 'affiliates.email')
    affiliates_api_key = await ConfigsORM.find_or_new(nome = 'affiliates.api_key')
    scripts_extras = await ConfigsORM.find_or_new(nome = 'scripts.extras')

    styles = await StylesORM.find_one()

    response = TenantIntegrationsResponse(
        tenant = {'name': config_data.nome},
        google_analytics_id = google_analytics_id.valor or "",
        google_gtm_id = google_gtm_id.valor or "",
        facebook_app_id = facebook_app_id.valor or "",
        facebook_app_secret = facebook_app_secret.valor or "",
        affiliates_email = affiliates_email.valor or "",
        affiliates_api_key = affiliates_api_key.valor or "",
        scripts_extras = scripts_extras.valor or "",
        facebook_widget = styles.facebook_widget or ""
    )
    tenancy_end()

    return response


@router.put('/tenants/{tenant_id}/management/integrations', status_code = 201, name = 'Edita as integrações de uma instancia', response_model = TenantIntegrationsResponse, tags = ['Tenants'])
@router.put('/backoffice/tenants/{tenant_id}/management/integrations', status_code = 201, name = 'Edita as integrações de uma instancia', response_model = TenantIntegrationsResponse, tags = ['Backoffice'])
async def tenant_integrations_edit(params: TenantIntegrations, tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id = tenant_id, created_by = user.id)
    product = await ProductsORM.find_one(tenant_id = tenant_id)
    if not product: raise HTTPException(status_code = 404, detail = 'Product not found')
    
    tenant = await TenantsORM.find_one(id = product.tenant_id)
    if not tenant: raise HTTPException(status_code = 404, detail = 'Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])
    config_data = await ConfigDataORM.find_one();

    google_analytics_id = await ConfigsORM.find_one(nome = 'google.analytics_id')
    await ConfigsORM.update(google_analytics_id.id, valor = params.google_analytics_id)

    google_gtm_id = await ConfigsORM.find_one(nome = 'google.gtm_id')
    await ConfigsORM.update(google_gtm_id.id, valor = params.google_gtm_id)

    facebook_app_id = await ConfigsORM.find_one(nome = 'facebook.app_id')
    await ConfigsORM.update(facebook_app_id.id, valor = params.facebook_app_id)

    facebook_app_secret = await ConfigsORM.find_one(nome = 'facebook.app_secret')
    await ConfigsORM.update(facebook_app_secret.id, valor = params.facebook_app_secret)

    affiliates_email = await ConfigsORM.find_one(nome = 'affiliates.email')
    await ConfigsORM.update(affiliates_email.id, valor = params.affiliates_email)

    affiliates_api_key = await ConfigsORM.find_one(nome = 'affiliates.api_key')
    await ConfigsORM.update(affiliates_api_key.id, valor = params.affiliates_api_key)

    scripts_extras = await ConfigsORM.find_one(nome = 'scripts.extras')
    await ConfigsORM.update(scripts_extras.id, valor = params.scripts_extras)

    styles = await StylesORM.find_one()
    await StylesORM.update(styles.id, facebook_widget = params.facebook_widget)

    response = TenantIntegrationsResponse(
        tenant = {'name': config_data.nome},
        **params.dict()
    )
    tenancy_end()

    return response

