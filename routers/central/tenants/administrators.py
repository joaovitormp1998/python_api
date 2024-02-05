from routers.central.tenants import router
from fastapi import Depends, HTTPException, Path, Query

from database import tenancy_initialize, tenancy_end
from database.central.products import ProductsORM
from database.central.tenants import TenantsORM
from database.tenant.users import UsersORM
from database.tenant.profiles import ProfileORM
from models.central.tenants import TenantAdminUserCreate, TenantAdminUserUpdate, TenantAdminUser, TenantAdminProfile, TenantAdminResponse
from utils.jwt_token import has_authenticated
import hashlib
import os
def old_password_hash(app_salt, human_password):
    if len(human_password) == 0:
        return None

    hashed_password = hashlib.sha1((app_salt + human_password).encode('utf-8')).hexdigest()
    return hashed_password


async def get_admins(tenant):
    tenancy_initialize(tenant.data['tenancy_db_name'])

    users = await UsersORM.find_many()
    profiles = await ProfileORM.find_many()
    profiles_dict = {p.id: p.nome for p in profiles}

    admins = []
    excluded_profile_ids = {3, 7}

    for user in users:
        if user.perfil_id not in excluded_profile_ids:
            admin = TenantAdminUser(
                id=user.id,
                name=user.nome,
                email=user.username,
                profile=profiles_dict[user.perfil_id],
                profile_id=user.perfil_id
            )
            admins.append(admin)

    filtered_profiles = {
        i: n for i, n in profiles_dict.items() if i not in excluded_profile_ids}
    tenant_admin_profiles = [TenantAdminProfile(
        id=i, name=n) for i, n in filtered_profiles.items()]

    data = TenantAdminResponse(users=admins, profiles=tenant_admin_profiles)
    tenancy_end()

    return data


async def get_students(tenant):
    tenancy_initialize(tenant.data['tenancy_db_name'])

    users = await UsersORM.find_many()
    profiles = await ProfileORM.find_many()
    profiles_dict = {p.id: p.nome for p in profiles}

    students = []
    student_profile_id = 3  # O ID do perfil para estudantes
    for user in users:
        if user.perfil_id == student_profile_id:
            student = TenantStudent(
                id=user.id,
                name=user.nome,
                email=user.username,
                profile=profiles_dict[user.perfil_id],
                profile_id=user.perfil_id
            )
            students.append(student)

    data = TenantStudentResponse(students=students)
    tenancy_end()

    return data


async def get_professors(tenant):
    tenancy_initialize(tenant.data['tenancy_db_name'])

    users = await UsersORM.find_many()
    profiles = await ProfileORM.find_many()
    profiles_dict = {p.id: p.nome for p in profiles}

    professors = []
    professor_profile_id = 7  # O ID do perfil para professores
    for user in users:
        if user.perfil_id == professor_profile_id:
            professor = TenantProfessor(
                id=user.id,
                name=user.nome,
                email=user.username,
                profile=profiles_dict[user.perfil_id],
                profile_id=user.perfil_id
            )
            professors.append(professor)

    data = TenantProfessorResponse(professors=professors)
    tenancy_end()

    return data


@router.get('/tenants/{tenant_id}/management/administrators', status_code=200, name='Obtem os administradores de uma instancia', response_model=TenantAdminResponse, tags=['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/administrators', status_code=200, name='Obtem os administradores de uma instancia', response_model=TenantAdminResponse, tags=['Backoffice'])
async def tenant_admins(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Produto not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    return await get_admins(tenant)


@router.get('/tenants/{tenant_id}/management/students', status_code=200, name='Obtem os Alunos de uma instancia', response_model=TenantAdminResponse, tags=['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/students', status_code=200, name='Obtem os Alunos de uma instancia', response_model=TenantAdminResponse, tags=['Backoffice'])
async def tenant_admins(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    return await get_students(tenant)


@router.get('/tenants/{tenant_id}/management/professors', status_code=200, name='Obtem os Professores de uma instancia', response_model=TenantAdminResponse, tags=['Tenants'])
@router.get('/backoffice/tenants/{tenant_id}/management/professors', status_code=200, name='Obtem os Professores de uma instancia', response_model=TenantAdminResponse, tags=['Backoffice'])
async def tenant_admins(tenant_id: str, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    return await get_professors(tenant)


@router.post('/tenants/{tenant_id}/management/administrators', status_code=201, name='Cria um novo administrador para instancia', response_model=TenantAdminResponse, tags=['Tenants'])
@router.post('/backoffice/tenants/{tenant_id}/management/administrators', status_code=201, name='Cria um novo administrador para instancia', response_model=TenantAdminResponse, tags=['Backoffice'])
async def tenant_admin_create(tenant_id: str, params: TenantAdminUserCreate, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    print(product)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])
    
    # Obtenha o valor de APP_SALT do ambiente ou de outra fonte
    app_salt = os.environ.get('APP_SALT', '')

    hashed_password = old_password_hash(app_salt, params.password)

    user = await UsersORM.create(
        nome=params.name,
        username=params.email,
        password=hashed_password,  # Use o hash da senha em vez da senha original
        perfil_id=params.profile_id
    )

    tenancy_end()

    return await get_admins(tenant)


@router.put('/tenants/{tenant_id}/management/administrators/{user_id}', status_code=201, name='Edita um administrador da instancia', response_model=TenantAdminResponse, tags=['Tenants'])
@router.put('/backoffice/tenants/{tenant_id}/management/administrators/{user_id}', status_code=201, name='Edita um administrador da instancia', response_model=TenantAdminResponse, tags=['Backoffice'])
async def tenant_admin_updated(tenant_id: str, user_id: int, params: TenantAdminUserCreate, user: dict = Depends(has_authenticated)):
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])
    app_salt = os.environ.get('APP_SALT', '')

    hashed_password = old_password_hash(app_salt, params.password)

    # Obtenha o usuário que você deseja atualizar
    user_to_update = await UsersORM.find_one(id=user_id)
    if not user_to_update:
        raise HTTPException(status_code=404, detail='User not found')

    # Construa o payload corretamente
    payload = {
        'nome': params.name,
        'username': params.email,
        'perfil_id': params.profile_id,
        'password': hashed_password,
    }

    # Atualize o usuário com o novo payload
    updated_user = await UsersORM.update(user_id, **payload)
    tenancy_end()

    return await get_admins(tenant)

@router.delete('/tenants/{tenant_id}/management/administrators/{user_id}', status_code=201, name='Excluir um administrador da instancia', response_model=TenantAdminResponse, tags=['Tenants'])
# @router.delete('/backoffice/tenants/{tenant_id}/management/administrators/{user_id}', status_code = 201, name = 'Excluir um administrador da instancia', response_model = TenantAdminResponse, tags = ['Backoffice'])
async def tenant_admin_delete(tenant_id: str, user_id: int, user: dict = Depends(has_authenticated)):
    # product = await ProductsORM.find_one(tenant_id=tenant_id, created_by=user.id)
    product = await ProductsORM.find_one(tenant_id=tenant_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    tenant = await TenantsORM.find_one(id=product.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    tenancy_initialize(tenant.data['tenancy_db_name'])

    user = await UsersORM.delete(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    tenancy_end()
    return await get_admins(tenant)


@router.patch('/tenants/{tenant_id}/management/owner', status_code=200, name='Atualiza Dono_enable de um Curso', tags=['Tenants'])
@router.patch('/backoffice/tenants/{tenant_id}/management/owner', status_code=200, name='Atualiza Dono de um Curso', tags=['Backoffice'])
async def update_owner(
        tenant_id: str,
        created_by: int = Query(..., title="ID do Novo Dono",
                                description="ID do Novo Dono"),
        user: dict = Depends(has_authenticated)
):
    product = await ProductsORM.find_one(tenant_id=tenant_id)

    if product:
        product.created_by = created_by
        await product.update(id=product.id, created_by=created_by)  # Corrected line

        return {'product': product}
    else:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
