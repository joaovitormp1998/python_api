from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import encode, decode
from passlib.context import CryptContext
from hashlib import sha1
from datetime import datetime, timedelta

from models.central.user import UserToken

from dotenv import load_dotenv
from os import getenv

load_dotenv()

JWT_SECRET = getenv('JWT_SECRET')
ALGORITHM = getenv('ALGORITHM') or 'HS256'

class Cryptor(CryptContext):
    def password_hash(self, password: str):
        return self.hash(password)

    def password_verify(self, password: str, hashed_password: str):
        print(self.identify(hashed_password))
        if not self.identify(hashed_password):
            return sha1(password.encode()).hexdigest() == hashed_password
        
        return self.verify(password, hashed_password)


password_hash = Cryptor(schemes = ["bcrypt"], deprecated = "auto")


def create_jwt(user) -> str:
    data = UserToken(**user.dict()).dict()
    data.pop('token')
     # Adiciona o tempo de expiração de 60 minutos  ao token
    expiration_time = datetime.utcnow() + timedelta(minutes=60)

    token_data = {
        "exp": expiration_time,
        **data
    }
    token = encode(data, JWT_SECRET, algorithm = ALGORITHM)
    return token


async def has_authenticated(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserToken:
    try:
        token = auth.credentials
        user = decode(token, JWT_SECRET, algorithms = [ALGORITHM])
        # Verifica se o token expirou
        expiration_time = user.get('exp', None)
        if expiration_time and datetime.utcnow() > datetime.utcfromtimestamp(expiration_time):
            raise HTTPException(status_code=401, detail="Token JWT expirado")

        return UserToken(**user, token = token)
    
    except Exception: raise HTTPException(status_code = 401, detail = "Token JWT inválido")


async def has_admin(user: str = Depends(has_authenticated)) -> UserToken:
    if user.group_id == 650: return user
    raise HTTPException(status_code = 401, detail = "O acesso é restrito")


