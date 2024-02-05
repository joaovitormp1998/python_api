from routers.central.tenants import router
from fastapi import Depends, HTTPException, Path
from typing import List

from database import tenancy_initialize, tenancy_end
from database.central.products import ProductsORM
from database.central.tenants import TenantsORM
from database.tenant.courses import CoursesORM
from database.tenant.config_data import ConfigDataORM
from database.tenant.configs import ConfigsORM
from models.central.tenants import TenantSeo, TenantSeoResponse, TenantCourseResponse
from utils.jwt_token import has_authenticated


@router.get('/tenants/{tenant_id}/management/seo', status_code=200, name='Obtem o SEO de uma instancia', response_model=TenantSeoResponse, tags=['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/seo', status_code=200, name='Obtem o SEO de uma instancia', response_model=TenantSeoResponse, tags=['Backoffice'])
async def tenant_seo(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])
    config_data = await ConfigDataORM.find_one()
    meta_description = await ConfigsORM.find_or_new(nome='meta.description')
    meta_keywords = await ConfigsORM.find_or_new(nome='meta.keywords')

    response = TenantSeoResponse(
        tenant={'name': config_data.nome},
        meta_description=meta_description.valor or "",
        meta_keywords=meta_keywords.valor or ""
    )
    tenancy_end()

    return response


@router.get('/tenants/{tenant_id}/management/courses', status_code=200, name='Obtem os Cursos de uma instancia', response_model=List[TenantCourseResponse], tags=['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/courses', status_code=200, name='Cursos o de uma instancia', response_model=List[TenantCourseResponse], tags=['Backoffice'])
async def tenant_courses(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    print(product)

    tenant = await TenantsORM.find_one(id=tenant_id)
    tenancy_initialize(tenant.data['tenancy_db_name'])

    courses = await CoursesORM.find_many()

    course_list = []
    for course in courses:
        course_dict = {
            'id': course.id,
            'nome': course.nome,
            'price_visible_enable': course.price_visible_enable,
            'status': course.status,
            'valor': course.valor
        }
        course_list.append(course_dict)

    tenancy_end()

    return course_list


@router.patch('/tenants/{tenant_id}/management/courses/{course_id}', status_code=200, name='Atualiza price_visible_enable de um Curso', response_model=TenantCourseResponse, tags=['Tenants'])
@router.patch('/backoffice/tenants/{tenant_id}/management/courses/{course_id}', status_code=200, name='Atualiza price_visible_enable de um Curso', response_model=TenantCourseResponse, tags=['Backoffice'])
async def update_course_price_visible(
        tenant_id: str,
        course_id: int = Path(..., title="ID do Curso",
                              description="ID do curso a ser atualizado"),
        price_visible_enable: bool = ...,
        user: dict = Depends(has_authenticated)
):
    # Encontrar o inquilino pelo ID
    tenant = await TenantsORM.find_one(id=tenant_id)

    if not tenant:
        raise HTTPException(status_code=404, detail="Inquilino não encontrado")

    # Inicializar a tenancy com o banco de dados específico do inquilino
    tenancy_initialize(tenant.data['tenancy_db_name'])

    try:
        # Encontrar o curso pelo ID
        course = await CoursesORM.find_one(id=course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Curso não encontrado")

        # Atualizar a visibilidade do preço do curso
        course.price_visible_enable = price_visible_enable
        await course.update(id=course_id, price_visible_enable=price_visible_enable)

        # Criar um dicionário com informações do curso atualizado
        course_dict = {
            'id': course.id,
            'nome': course.nome or "",
            'price_visible_enable': course.price_visible_enable or True,
            'status': course.status or "",
            'valor': course.valor or 0

        }

        # Finalizar a tenancy
        tenancy_end()

        return course_dict

    except Exception as e:
        # Finalizar a tenancy em caso de erro
        tenancy_end()
        raise HTTPException(
            status_code=500, detail=f"Erro durante a atualização do curso: {str(e)}")

# Atualizar dono 

@router.put('/tenants/{tenant_id}/management/seo', status_code=201, name='Edita o SEO de uma instancia', response_model=TenantSeoResponse, tags=['Tenants'])
@router.put('/backoffice/tenants/{tenant_id}/management/seo', status_code=201, name='Edita o SEO de uma instancia', response_model=TenantSeoResponse, tags=['Backoffice'])
async def tenant_seo_edit(params: TenantSeo, tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])
    config_data = await ConfigDataORM.find_one()

    meta_description = await ConfigsORM.find_one(nome='meta.description')
    await ConfigsORM.update(meta_description.id, valor=params.meta_description)

    meta_keywords = await ConfigsORM.find_one(nome='meta.keywords')
    await ConfigsORM.update(meta_keywords.id, valor=params.meta_keywords)

    response = TenantSeoResponse(
        tenant={'name': config_data.nome},
        **params.dict()
    )
    tenancy_end()

    return response
