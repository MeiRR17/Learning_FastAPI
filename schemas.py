from datetime import datetime
from typing import Optional

from pydantic import BaseModel, confloat, constr, validator


ItemName = constr(strip_whitespace=True, min_length=1, max_length=120)
ItemPrice = confloat(ge=0, allow_inf_nan=False)
ItemDescription = constr(max_length=2000)


class ItemBase(BaseModel):
    name: ItemName
    description: Optional[ItemDescription] = None
    price: ItemPrice


class ItemCreate(ItemBase):
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: Optional[ItemName] = None
    description: Optional[ItemDescription] = None
    price: Optional[ItemPrice] = None
    in_stock: Optional[bool] = None

    @validator("name", "price", "in_stock", pre=True)
    def reject_null_for_required_database_fields(cls, value):
        # Omitted update fields are fine. Explicit JSON null must never
        # replace a non-nullable response field in the database.
        if value is None:
            raise ValueError("This field cannot be null; omit it instead")
        return value


class ItemResponse(ItemBase):
    id: int
    in_stock: bool
    created_at: datetime

    class Config:
        from_attributes = True
