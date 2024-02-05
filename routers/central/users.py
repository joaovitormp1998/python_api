from fastapi import APIRouter, Depends, HTTPException

from database.central.users import UserORM
from database.central.products import ProductsORM
from database.central.address import AddressORM
from database.central.tenants import TenantsORM
from database.central.domains import DomainsORM
from utils.jwt_token import has_admin, password_hash, has_authenticated

router = APIRouter(prefix='/api/backoffice')


async def get_tenants_backoffice(products):
    tenants = []
    for product in products:

        tenant = await TenantsORM.find_one(id=product.tenant_id)
        if not tenant:
            continue

        domain = await DomainsORM.find_one(tenant_id=product.tenant_id)
        if not domain:
            continue

        owner = await UserORM.find_one(id=product.created_by)
        partner = await UserORM.find_one(id=tenant.partner_id)
        administrator = await UserORM.find_one(id=tenant.administrator_id)
        service = await UserORM.find_one(id=tenant.service_id)
        finance = await UserORM.find_one(id=tenant.finance_id)

        data = {
            'id': product.tenant_id,
            'name': product.name,
            'domain': domain.domain,
            'created_at': tenant.created_at,
            'active': domain.status,
            'owner': owner.name,
            'partner': partner.name if partner else None,
            'administrator': administrator.name if administrator else None,
            'service': service.name if service else None,
            'finance': finance.name if finance else None
        }

        tenants.append(data)

    return tenants


@router.get('/users', status_code=200, name='Buscar clientes', tags=['Backoffice'])
async def users(sudo: dict = Depends(has_authenticated)):
    products = await ProductsORM.find_many(type='tenant')
    users = await UserORM.find_many()
    response = []

    for user in users:
        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'last_name': user.last_name,
            'site': len([i for i in products if i.created_by == user.id])
        }

        response.append(data)

    return response


@router.get('/users/{user_id}', status_code=200, name='Cliente', tags=['Backoffice'])
async def user(user_id: int, sudo: dict = Depends(has_authenticated)):
    user = await UserORM.find_one(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    products = await ProductsORM.find_many(created_by=user_id, type='tenant')
    address = await AddressORM.find_one(user_id=user_id)

    response = {
        'name': user.name,
        'last_name': user.last_name,
        'email': user.email,
        'photo': user.photo,
        'phone': user.phone,
        'document': user.document,
        'tenants': await get_tenants_backoffice(products),
        'zip_code': address.zip_code if address else None,
        'city': address.city if address else None,
        'state': address.state if address else None,
        'address_line': address.address_line if address else None,
        'address_line_2': address.address_line_2 if address else None
    }

    return response


@router.delete('/users/{user_id}', status_code=204, name='Deletar Cliente', tags=['Backoffice'])
async def delete_user(user_id: int, sudo: dict = Depends(has_authenticated)):
    user = await UserORM.find_one(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    # Aqui você pode adicionar a lógica para deletar o usuário
    await UserORM.delete(id=user.id)

    return None


@router.post('/users', status_code=201, name='Criar cliente', tags=['Backoffice'])
async def create_user(user_data: dict, sudo: dict = Depends(has_authenticated)):

    # Validate user_data
    required_fields = ['name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in user_data:
            raise HTTPException(
                status_code=422, detail=f"Missing required field: {field}")

    # Check if the user with the given email already exists
    existing_user = await UserORM.find_one(email=user_data['email'])
    if existing_user:
        raise HTTPException(status_code=400, detail="O email já está em uso")

    pass_hash = password_hash.hash(user_data['password'])

    # Create the new user in the database
    new_user_data = {
        'name': user_data['name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'password': pass_hash,
        # Add other fields as needed
    }
    new_user = await UserORM.create(**new_user_data, group_id=1)

    # Return a response with the new user's information
    return {'message': 'User created successfully', 'user_id': new_user.id}
@router.put('/users/{user_id}', status_code=200, name='Atualizar Cliente', tags=['Backoffice'])
async def update_user(user_id: int, user_data: dict, sudo: dict = Depends(has_authenticated)):
    # Verificar se o usuário existe
    existing_user = await UserORM.find_one(id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    # Validar dados do usuário
    required_fields = ['name', 'last_name', 'email']
    for field in required_fields:
        if field not in user_data:
            raise HTTPException(
                status_code=422, detail=f"Campo obrigatório ausente: {field}")

    # Verificar se o novo endereço de e-mail já está em uso por outro usuário
    if 'email' in user_data and user_data['email'] != existing_user.email:
        existing_email_user = await UserORM.find_one(email=user_data['email'])
        if existing_email_user:
            raise HTTPException(
                status_code=400, detail="O email já está em uso por outro usuário")

    # Atualizar os dados do usuário no banco de dados
    await existing_user.update(id=user_id,**user_data)

    # Recuperar os dados atualizados do usuário
    updated_user = await UserORM.find_one(id=user_id)

    # Retornar uma resposta com as informações atualizadas do usuário
    return {
        'message': 'Usuário atualizado com sucesso',
        'user_id': updated_user.id,
        'name': updated_user.name,
        'last_name': updated_user.last_name,
        'email': updated_user.email
        # Adicione outros campos conforme necessário
    }
