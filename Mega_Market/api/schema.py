from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ShopUnitType(str, Enum):
    offer = "OFFER"
    category = "CATEGORY",

    class Config:
        orm_mode = True


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

