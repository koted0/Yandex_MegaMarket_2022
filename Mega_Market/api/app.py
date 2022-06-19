from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from Mega_Market.api.database import SessionLocal, engine
from uuid import UUID
from . import schema, model, crud


app = FastAPI()

model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/imports')
def import_shop_unit(shop_unit_request: schema.ShopUnitImportRequest, db: Session = Depends(get_db)):
    return crud.post_shop_unit(shop_unit_request, db)


@app.delete('/delete/{shop_unit_id}')
def delete_id(shop_unit_id: UUID, db: Session = Depends(get_db)):
    crud.delete_item_from_db(shop_unit_id, db)


@app.get('/nodes/{shop_unit_id}')
def get_shop_unit_by_id(shop_unit_id: UUID, db: Session = Depends(get_db)) -> schema.ShopUnit:
    return crud.get_item_from_db(shop_unit_id, db)
