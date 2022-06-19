from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

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
    shop_unit = db.query(model.ShopUnit).filter(model.ShopUnit.id == shop_unit_id).first()
    if not shop_unit:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(shop_unit)
    db.commit()


def get_items_from_db(shop_unit_id: UUID, db: Session):
    result = (db.execute('WITH RECURSIVE category_path (id, name, price, date, type, "parentId") AS'
                      '('
                      'SELECT id, name, price, date, type, "parentId" '
                      'FROM shop_unit '
                      f"Where id = '{shop_unit_id}' "
                      'UNION ALL '
                      'SELECT c.id, c.name, c.price, c.date, c.type, c."parentId"'
                      'FROM category_path AS cp JOIN shop_unit AS c '
                      'ON cp.id = c."parentId") '
                      'SELECT * FROM category_path'))

    return result


@app.get('/nodes/{shop_unit_id}')
def get_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)) -> schema.ShopUnit:
    result = get_items_from_db(shop_unit_id, db)
    output = {}
    for item in result:
        output[item.id] = schema.ShopUnit(
            id=item.id,
            name=item.name,
            parentId=item.parentId,
            price=item.price,
            date=item.date,
            type=item.type,
        )

    root = None

    for key, item in output.items():
        if item.parentId in output:
            if output[item.parentId].children is None:
                output[item.parentId].children = []
            output[item.parentId].children.append(item)
        else:
            root = item
    return root
