from fastapi import APIRouter, Depends, HTTPException
from typing import List

from models.central.chamados import Chamado, ChamadoResponse
from database.central.chamados import ChamadosORM
from database.central.users import UserORM
from utils.jwt_token import has_authenticated, has_admin

router = APIRouter(prefix='/api/chamados')


async def get_chamados():
    chamados = await ChamadosORM.find_many()

    result = []
    for chamado in chamados:
        user = await UserORM.find_one(id=chamado.created_by)
        if user:
            user_name = user.name
            chamado_response = ChamadoResponse(
                cliente=user_name, **chamado.dict())
            result.append(chamado_response)

    return result


@router.get('/', status_code=200, name='Lista de chamados', response_model=List[ChamadoResponse], tags=['Chamados'])
async def chamados_list(user: dict = Depends(has_authenticated)):
    return await get_chamados()


@router.post('/', status_code=201, name='Cria um chamado', response_model=List[ChamadoResponse], tags=['Chamados'])
async def chamado_create(chamado: Chamado, user: dict = Depends(has_authenticated)):
    await ChamadosORM.create(**chamado.dict())
    return await get_chamados()


@router.put('/{chamado_id}', status_code=200, name='Edita um chamado', response_model=List[ChamadoResponse], tags=['Chamados'])
async def chamado_update(chamado_id: int, chamado: Chamado, user: dict = Depends(has_authenticated)):
    await ChamadosORM.update(chamado_id, **chamado.dict())
    return await get_chamados()


@router.delete('/{chamado_id}', status_code=200, name='Exclui um chamado', response_model=List[ChamadoResponse], tags=['Chamados'])
async def chamado_delete(chamado_id: int, user: dict = Depends(has_authenticated)):
    await ChamadosORM.delete(id=chamado_id)
    return await get_chamados()


@router.get('/{chamado_id}', status_code=200, name='Obtém um chamado', response_model=ChamadoResponse, tags=['Chamados'])
async def chamado_detail(chamado_id: int, user: dict = Depends(has_authenticated)):
    chamado = await ChamadosORM.find_one(id=chamado_id)
    return ChamadoResponse(**chamado.dict())
