from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from analyzer.api.database import SessionLocal, engine
from uuid import UUID
from . import schemas, models, crud, shop_service
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/imports', response_model=schemas.ShopUnitImportRequest)
async def import_shop_unit(shop_unit_request: schemas.ShopUnitImportRequest, db: Session = Depends(get_db)):
    crud.post_item_to_db(shop_unit_request, db)


@app.delete('/delete/{shop_unit_id}')
async def delete_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)):
    crud.delete_item_from_db(shop_unit_id, db)


@app.get('/nodes/{shop_unit_id}',
         response_model=schemas.ShopUnit,
         responses={
            404: {'model': schemas.Error, "content": {
                "application/json": {
                    "example": {'code': 404, "message": "No item found"}
                }}
            },
         })
async def get_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)) -> schemas.ShopUnit:
    exist = shop_service.find_unit(shop_unit_id, db)
    if not exist:
        return schemas.NoItemsError()

    return crud.get_item_from_db(shop_unit_id, db)


@app.get('/sales', response_model=schemas.ShopUnitStatisticResponse)
async def get_sales(date: datetime, db: Session = Depends(get_db)) -> schemas.ShopUnit:
    return crud.get_sales_from_db(date, db)


@app.get('/node/{id}/statistic',
         response_model=schemas.ShopUnitStatisticResponse,
         responses={
             404: {'model': schemas.Error, "content": {
                "application/json": {
                    "example": {'code': 404, "message": "No item found"}
                }
            }},
         })
def get_statistic(shop_unit_id: UUID, date_start: datetime,
                  date_end: datetime, db: Session = Depends(get_db)) -> schemas.ShopUnitStatisticResponse:
    data = crud.get_statistic(shop_unit_id, date_start, date_end, db)
    if not data:
        return schemas.NoItemsError()

    return data