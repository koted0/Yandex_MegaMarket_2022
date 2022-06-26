from datetime import datetime
from enum import Enum
from typing import List, Optional, Any
from uuid import UUID

from fastapi.responses import JSONResponse
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


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID]
    type: ShopUnitType
    price: Optional[int]
    date: datetime

    class Config:
        orm_mode = True


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]

    class Config:
        orm_mode = True


class Error(BaseModel):
    code: int
    message: str


class NoItemsError(JSONResponse):
    def __init__(self):
        super().__init__(status_code=404, content={'code': 404, 'message': 'Item not found'})
