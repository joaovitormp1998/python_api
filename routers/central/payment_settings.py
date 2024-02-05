from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.central.payment_settings import PaymentSettings, PaymentSettingsResponse
from database.central.payment_settings import PaymentSettingsORM
from utils.jwt_token import has_authenticated, has_admin

router = APIRouter(prefix='/api')

async def get_payment_settings():
    payment_settings = await PaymentSettingsORM.find_many()
    return [PaymentSettingsResponse(**p.dict()) for p in payment_settings]

@router.get('/payment_settings', status_code=200, name='Obtém configurações de pagamento', response_model=List[PaymentSettingsResponse], tags=['Central - Pagamentos - Configurações'])
@router.get('/central/payment_settings', status_code=200, name='Configurações de Pagamento', tags=['Central - Pagamentos - Configurações'])
async def payment_settings_list(user: dict = Depends(has_authenticated)):
    return await get_payment_settings()

@router.put('/central/payment_settings/{payment_settings_id}', status_code=200, name='Edita configurações de pagamento', response_model=List[PaymentSettingsResponse], tags=['Central - Pagamentos - Configurações'])
async def update_payment_settings(payment_settings_id: int, params: PaymentSettings, admin: dict = Depends(has_admin)):
    await PaymentSettingsORM.update(id=payment_settings_id, **params.dict())
    return await get_payment_settings()

@router.get('/central/payment_settings/{payment_settings_id}', status_code=200, name='Obtém configurações de pagamento', response_model=PaymentSettingsResponse, tags=['Central - Pagamentos - Configurações'])
async def get_payment_settings_by_id(payment_settings_id: int, admin: dict = Depends(has_admin)):
    payment_settings = await PaymentSettingsORM.find_one(id=payment_settings_id)
    return PaymentSettingsResponse(**payment_settings.dict())
