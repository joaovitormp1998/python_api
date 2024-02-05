from fastapi import APIRouter, Depends, HTTPException

from models.central.categorias import Categorias, CategoriasResponse
from database.central.categorias import CategoriasORM
from utils.jwt_token import has_authenticated, has_admin

from typing import List

router = APIRouter(prefix = '/api')

async def get_categorias():
    categorias = await CategoriasORM.find_many()
    return [CategoriasResponse(**p.dict()) for p in categorias]



@router.get('/backoffice/categorias', status_code = 200, name = 'Lista categorias', response_model = List[CategoriasResponse], tags = ['Backoffice - Categorias de Produtos'])
async def categorias(admin: dict = Depends(has_admin)):
    return await get_categorias()

@router.post('/backoffice/categorias', status_code = 201, name = 'Cria uma Categoria', response_model = List[CategoriasResponse], tags = ['Backoffice - Categorias de Produtos'])
async def plan_create(params: Categorias, admin: dict = Depends(has_admin)):
    await CategoriasORM.create(**params.dict())
    return await get_categorias()