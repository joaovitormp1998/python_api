from pydantic import BaseModel
from typing import Optional, List


class StorageResponse(BaseModel):
    used: Optional[str] = '0.0GB'


class SiteResponse(BaseModel):
    id: str
    name: str
    domain: str
    disabled_at: int = 0
    status: str
    icon: Optional[str] = None
    type: str
    students: int
    storage: Optional[StorageResponse] = StorageResponse()
    token: Optional[str] = None


class TenantsResponse(BaseModel):
    used_storage: str = '0.0GB'
    students: int = 0
    activated: int = 0
    sites: List[SiteResponse] = []
    

class TenantCreate(BaseModel):
    name: str
    tenant_id: str
    plan: int = 1
    tenant_password: str


class DomainUpdate(BaseModel):
     status:str
class TenantResponseBase(BaseModel):
    name: str


class TenantGeneralResponseBase(TenantResponseBase):
    domain: str
    users: int
    status: str

class TenantGeneral(BaseModel):
    name: str
    phone: str
    is_whatsApp: bool
    whatsapp_message: str
    address: str
    zipcode: str
    cnpj: str
    email: str
    service: str
    domain: str
    

class TenantGeneralResponse(TenantGeneral):
    tenant: TenantGeneralResponseBase


class TenantIntegrations(BaseModel):
    google_analytics_id: str
    google_gtm_id: str
    facebook_app_id: str
    facebook_app_secret: str
    affiliates_email: str
    affiliates_api_key: str
    scripts_extras: str
    facebook_widget: str
    

class TenantIntegrationsResponse(TenantIntegrations):
    tenant: TenantResponseBase


class TenantSeo(BaseModel):
    meta_description: str
    meta_keywords: str


class TenantSeoResponse(TenantSeo):
    tenant: TenantResponseBase


class TenantAdminUserBase(BaseModel):
    name: str
    email: str
    profile: str
    profile_id: int = 1


class TenantAdminUserCreate(TenantAdminUserBase):
    password: str


class TenantAdminUserUpdate(TenantAdminUserBase):
    password: Optional[str] = None


class TenantAdminUser(TenantAdminUserBase):
    id: int


class TenantAdminProfile(BaseModel):
    id: int
    name: str


class TenantAdminResponse(BaseModel):
    users: List[TenantAdminUser]
    profiles: List[TenantAdminProfile]
    
class TenantCourseResponse(BaseModel):
    id:int
    nome:str
    price_visible_enable:bool
    status:str
    valor:float