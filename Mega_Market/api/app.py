from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Mega_Market.api.database import SessionLocal, engine
from uuid import UUID
from . import schemas, models, crud, shop_service
from datetime import datetime

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/imports')
def import_shop_unit(shop_unit_request: schemas.ShopUnitImportRequest, db: Session = Depends(get_db)):
    crud.post_item_to_db(shop_unit_request, db)


@app.delete('/delete/{shop_unit_id}')
def delete_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)):
    crud.delete_item_from_db(shop_unit_id, db)


@app.get('/nodes/{shop_unit_id}', response_model=schemas.ShopUnit)
def get_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)) -> schemas.ShopUnit:
    flat_units = shop_service.find_unit(shop_unit_id, db)
    if not flat_units:
        raise HTTPException(status_code=404, detail="Item not found")

    return crud.get_item_from_db(shop_unit_id, db)


@app.get('/sales')
def get_sales(date: datetime, db: Session = Depends(get_db)) -> schemas.ShopUnit:
    return crud.get_sales_from_db(date, db)
