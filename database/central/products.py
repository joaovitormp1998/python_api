from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func, Enum
from database import Base, configure_metadata
from database.central.group import GroupORM

from models.central.user import UserSignUp
from sqlalchemy.orm import relationship

class ProductsORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'products'

    class TypeEnum(Enum):
        PHYSICAL = 'physical'
        DIGITAL = 'digital'
        TENANT = 'tenant'

    class AffiliateAmountTypeEnum(Enum):
        FLAT = 'flat'
        PERCENTAGE = 'percentage'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    # type = Column(TypeEnum)
    tenant_id = Column(String)
    amount = Column(Integer)
    landing_page_url = Column(String)
    download_url = Column(String)
    shipper_zip_code = Column(String)
    size = Column(JSON)
    weight = Column(Integer)
    max_qnt = Column(Integer)
    free_shipping = Column(Integer)
    affiliate_active = Column(Integer)
    affiliate_amount = Column(Integer)
    affiliate_amount_type = Column(String)
    # affiliate_amount_type = Column(AffiliateAmountTypeEnum)
    photo = Column(String)
    warranty_days = Column(Integer)
    created_by = Column(Integer)
    available = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    hidden = Column(Integer)
    plan_id = Column(Integer)
