from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ShopUnitType(str, Enum):
    offer = "OFFER"
    category = "CATEGORY",


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID]
    type: ShopUnitType
    price: Optional[int]

    class Config:
        orm_mode = True


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime

    class Config:
        orm_mode = True


class ShopUnit(ShopUnitImport):
    date: Optional[datetime]
    children: Optional[List["ShopUnit"]]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat().replace('+00:00', 'Z'),
        }

