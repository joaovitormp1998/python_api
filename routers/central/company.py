from fastapi import APIRouter, Depends, HTTPException

from models.central.company import Company, CompanyResponse
from database.central.company import CompanyORM
from database.central.users import UserORM
from utils.jwt_token import has_authenticated, has_admin

from typing import List

router = APIRouter(prefix='/api')


# async def get_companies():
#     companies = await CompanyORM.find_many()
#     return [CompanyResponse(**p.dict()) for p in companies]
async def get_companies():
    companies = await CompanyORM.find_many()

    result = []

    for company in companies:
        # Perform a find_one operation on UserORM to get user details
        user = await UserORM.find_one(id = company.created_by)

        if user:
            user_name = user.name
            company_response = CompanyResponse(dono=user_name, **company.dict())
            result.append(company_response)

    return result
async def get_company(company_id):
    company = await CompanyORM.find_one(id=company_id)
    user = await UserORM.find_one(id=company.created_by)
    
    user_name = user.name if user else None
    return CompanyResponse(dono=user_name, **company.dict())


@router.get('/companies', status_code=200, name='Lista empresas', response_model=List[CompanyResponse], tags=['Backoffice - Empresas'])
@router.get('/backoffice/companies', status_code=200, name='Empresas', tags=['Backoffice - Empresas'])
async def companies(user: dict = Depends(has_authenticated)):
    return await get_companies()


@router.post('/backoffice/companies', status_code=201, name='Cria um empresa', response_model=List[CompanyResponse], tags=['Backoffice - Empresas'])
async def plan_create(params: Company, admin: dict = Depends(has_admin)):
    await CompanyORM.create(**params.dict())
    return await get_companies()


@router.put('/backoffice/companies/{company_id}', status_code=201, name='Edita um empresa', response_model=List[CompanyResponse], tags=['Backoffice - Empresas'])
async def plan_create(company_id: int, params: Company, admin: dict = Depends(has_admin)):
    await CompanyORM.update(company_id, **params.dict())
    return await get_companies()


@router.delete('/backoffice/companies/{company_id}', status_code=201, name='Exclui um empresa', response_model=List[CompanyResponse], tags=['Backoffice - Empresas'])
async def plan_create(company_id: int, admin: dict = Depends(has_admin)):
    await CompanyORM.delete(id=company_id)
    return await get_companies()


@router.get('/backoffice/companies/{company_id}', status_code=200, name='Obtem um empresa', response_model=CompanyResponse, tags=['Backoffice - Empresas'])
async def plan_create(company_id: int, admin: dict = Depends(has_admin)):
    company = await CompanyORM.find_one(id=company_id)
    return await get_company(company_id)
