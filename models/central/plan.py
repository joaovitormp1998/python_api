from pydantic import BaseModel


class Plan(BaseModel):
    name: str
    description: str
    price: float
    max_students: int
    max_storage: int
    is_active: bool = True
    extra_storage: float
    extra_students: float


class PlanResponse(Plan):
    id: int