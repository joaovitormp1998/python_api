from fastapi import APIRouter, Depends, HTTPException

from models.central.user import UserProfile, Address
from database.central.users import UserORM
from database.central.address import AddressORM
from utils.jwt_token import has_authenticated
import logging
from starlette import status


logger = logging.getLogger(__name__)
router = APIRouter(prefix = '/api/profile', tags = ['Profile'])


@router.get('', status_code=200, name='Meu Perfil', response_model=UserProfile)
async def profile(user: dict = Depends(has_authenticated)):
    try:
        user_id = getattr(user, 'id', None)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

        logger.info(f"Received request for profile with user ID: {user_id}")
        
        user_instance = await UserORM.find_one(id=user_id)
        logger.debug(f"Retrieved user instance: {user_instance}")
        
        address = await AddressORM.find_one(user_id=user_id)
        logger.debug(f"Retrieved address instance: {address}")
        
        response = UserProfile(**user_instance.dict())
        
        if address:
            print('-------------------------------------------')
            print(address)
            print('-------------------------------------------')
            address_data = address.dict()
            print(address_data)
            address_data['address_line_2'] = address_data.get('address_line_2', '')  # Fornecer um valor padrão se for None
            response.address = Address(**address_data)
        
        logger.info("Returning profile response")
        return response
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    try:
        logger.info(f"Received request for profile with user ID: {user.get('id')}")
        
        user_instance = await UserORM.find_one(id=user['id'])
        logger.debug(f"Retrieved user instance: {user_instance}")
        
        address = await AddressORM.find_one(user_id=user['id'])
        logger.debug(f"Retrieved address instance: {address}")
        
        response = UserProfile(**user_instance.dict())
        
        if address:
            address_data = address.dict()
            address_data['address_line_2'] = address_data.get('address_line_2', '')  # Fornecer um valor padrão se for None
            response.address = Address(**address_data)
        
        logger.info("Returning profile response")
        return response
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put('', status_code = 201, name = 'Editar meu Perfil', response_model = UserProfile)
async def profile_edit(params: UserProfile, user: dict = Depends(has_authenticated)):
    data = params.dict()
    data.pop('address')
    await UserORM.update(user.id, **data)

    address = params.address.dict() if params.address else None

    if address:
        user_address = await AddressORM.find_one(user_id = user.id)
        if user_address: await AddressORM.update(user_address.id, **address)
        else: await AddressORM.create(user_id = user.id, **address)

    return params
