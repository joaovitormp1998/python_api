from fastapi import APIRouter, Depends, HTTPException

from models.central import user, auth
from database.central.users import UserORM
from utils.jwt_token import password_hash, create_jwt, has_authenticated

router = APIRouter(prefix = '/api/auth', tags = ['Auth'])


@router.post('/register', status_code = 201, name = 'Registrar-se', response_model = auth.AuthResponse)
async def register(params: auth.RegisterParameters):
    user = await UserORM.find_one(email = params.email)
    if user:
        raise HTTPException(status_code = 400, detail = 'O email já está em uso')

    params.password = password_hash.hash(params.password)
    data = await UserORM.create(**params.dict(), group_id = 1)
        
    token = create_jwt(data)
    user = auth.User(**data.dict())

    return auth.AuthResponse(user = user, access_token = token)


@router.post('/login', status_code = 201, name = 'Login', response_model = auth.AuthResponse)
async def login(params: auth.LoginParameters):
    user = await UserORM.find_one(email = params.email)
    
    if not user or not password_hash.password_verify(params.password, user.password):
            raise HTTPException(
            status_code = 401, detail = 'Credenciais inválidas')

    token = create_jwt(user)
    user = auth.User(**user.dict())

    return auth.AuthResponse(user = user, access_token = token)


@router.get('/me', status_code = 200, name = 'Meu Perfil', response_model = auth.AuthResponse)
async def profile(user: dict = Depends(has_authenticated)):
    return auth.AuthResponse(user = user.dict(), access_token = user.token)
