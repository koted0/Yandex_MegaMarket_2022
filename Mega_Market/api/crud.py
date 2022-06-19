import datetime

import pytz

from . import schema, model
from uuid import UUID
from sqlalchemy.orm import Session



def get_query_from_db(shop_unit_id: UUID, db: Session):
    return db.execute('WITH RECURSIVE category_path (id, name, price, date, type, "parentId") AS'
                      '('
                      'SELECT id, name, price, date, type, "parentId" '
                      'FROM shop_unit '
                      f"Where id = '{shop_unit_id}' "
                      'UNION ALL '
                      'SELECT c.id, c.name, c.price, c.date, c.type, c."parentId"'
                      'FROM category_path AS cp JOIN shop_unit AS c '
                      'ON cp.id = c."parentId") '
                      'SELECT * FROM category_path')


def make_model_from_schema(shop_unit: schema.ShopUnitImport, date):
    return model.ShopUnit(**shop_unit.dict(), date=date)


def post_shop_unit(shop_unit_request: schema.ShopUnitImportRequest, db: Session):
    for item in shop_unit_request.items:
        unit_model = make_model_from_schema(item, shop_unit_request.updateDate)
        if db.query(model.ShopUnit).filter_by(id=item.id).first() is None:
            db.add(unit_model)
        # else:
        #     db.query(model.ShopUnit).filter(model.ShopUnit.id == item.id).\
        #         update(unit_model)
    db.commit()


def delete_item_from_db(shop_unit_id: UUID, db: Session):
    db.delete(db.query(model.ShopUnit).filter(model.ShopUnit.id == shop_unit_id).first())
    db.commit()


def get_item_from_db(shop_unit_id: UUID, db: Session):
    query = get_query_from_db(shop_unit_id, db)
    formatted_query = {}
    for item in query:
        schema_item = schema.ShopUnit.from_orm(item)
        schema_item.date = pytz.UTC.localize(schema_item.date)
        formatted_query.update({item.id: schema_item}) # изменить на обычное заполнение
    # [formatted_query.update({item.id: schema.ShopUnit.from_orm(item)}) for item in query]

    root = None

    # Part for parents and children
    for key, item in formatted_query.items():
        if item.parentId in formatted_query:
            if formatted_query[item.parentId].children is None:
                formatted_query[item.parentId].children = []
            formatted_query[item.parentId].children.append(item)
        else:
            root = item
    return root
