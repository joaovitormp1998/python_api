from fastapi import APIRouter, Depends, HTTPException

from models.central.plan import Plan, PlanResponse
from database.central.plans import PlansORM
from utils.jwt_token import has_authenticated, has_admin

from typing import List

router = APIRouter(prefix = '/api')

async def get_plans():
    plans = await PlansORM.find_many()
    return [PlanResponse(**p.dict()) for p in plans]


@router.get('/plans', status_code = 200, name = 'Pega planos', response_model = List[PlanResponse], tags = ['Backoffice - Planos'])
@router.get('/backoffice/plans', status_code = 200, name = 'Planos', tags = ['Backoffice - Planos'])
async def plans(user: dict = Depends(has_authenticated)):
    return await get_plans()


@router.post('/backoffice/plans', status_code = 201, name = 'Cria um plano', response_model = List[PlanResponse], tags = ['Backoffice - Planos'])
async def plan_create(params: Plan, admin: dict = Depends(has_admin)):
    await PlansORM.create(**params.dict())
    return await get_plans()


@router.put('/backoffice/plans/{plan_id}', status_code = 201, name = 'Edita um plano', response_model = List[PlanResponse], tags = ['Backoffice - Planos'])
async def plan_create(plan_id: int, params: Plan, admin: dict = Depends(has_admin)):
    await PlansORM.update(plan_id, **params.dict())
    return await get_plans()


@router.delete('/backoffice/plans/{plan_id}', status_code = 201, name = 'Exclui um plano', response_model = List[PlanResponse], tags = ['Backoffice - Planos'])
async def plan_create(plan_id: int, admin: dict = Depends(has_admin)):
    await PlansORM.delete(id = plan_id)
    return await get_plans()


@router.get('/backoffice/plans/{plan_id}', status_code = 200, name = 'Obtem um plano', response_model = PlanResponse, tags = ['Backoffice - Planos'])
async def plan_create(plan_id: int, admin: dict = Depends(has_admin)):
    plan = await PlansORM.find_one(id = plan_id)
    return PlanResponse(**plan.dict())