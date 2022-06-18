from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from Mega_Market.api.database import SessionLocal, engine
from . import schemas, models

import datetime

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def shop_unit_to(shop_unit: schemas.ShopUnitImport, date: datetime):
    return models.ShopUnit(
        id=shop_unit.id,
        name=shop_unit.name,
        parentId=shop_unit.parentId,
        price=shop_unit.price,
        date=date,
        type=shop_unit.type,
    )


@app.post('/imports')
def import_shop_unit(shop_unit_request: schemas.ShopUnitImportRequest, db: Session = Depends(get_db)):
    for shop_unit in shop_unit_request.items:
        unit = shop_unit_to(shop_unit, shop_unit_request.updateDate)
        db.add(unit)
    db.commit()
