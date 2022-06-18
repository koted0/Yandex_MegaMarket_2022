from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from Mega_Market.api.database import SessionLocal, engine
from . import schema, model

import datetime
from uuid import UUID

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def shop_unit_to(shop_unit: schema.ShopUnitImport, date: datetime):
    return model.ShopUnit(
        id=shop_unit.id,
        name=shop_unit.name,
        parentId=shop_unit.parentId,
        price=shop_unit.price,
        date=date,
        type=shop_unit.type,
    )


@app.post('/imports')
def import_shop_unit(shop_unit_request: schema.ShopUnitImportRequest, db: Session = Depends(get_db)):
    for shop_unit in shop_unit_request.items:
        unit = shop_unit_to(shop_unit, shop_unit_request.updateDate)
        db.add(unit)
    db.commit()


@app.delete('/delete/{shop_unit_id}')
def delete_id(shop_unit_id: UUID, db: Session = Depends(get_db)):
    shop_unit = db.query(model.ShopUnit).filter(model.ShopUnit.id == shop_unit_id).delete()
    if not shop_unit:
        raise HTTPException(status_code=404, detail='Item not found')
    db.commit()  # TODO: удалять категории и все дочерние элементы


@app.get('/nodes/{shop_unit_id}')
def get_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)):
    return db.query(model.ShopUnit).filter(model.ShopUnit.id == shop_unit_id).first()
