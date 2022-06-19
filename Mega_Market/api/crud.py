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


def post_shop_unit(shop_unit_request: schema.ShopUnitImportRequest, db: Session):
    [db.add(model.ShopUnit(**shop_unit.dict(), date=shop_unit_request.updateDate))
     for shop_unit in shop_unit_request.items]
    db.commit()


def delete_item_from_db(shop_unit_id: UUID, db: Session):
    db.delete(db.query(model.ShopUnit).filter(model.ShopUnit.id == shop_unit_id).first())
    db.commit()


def get_item_from_db(shop_unit_id: UUID, db: Session):
    query = get_query_from_db(shop_unit_id, db)
    formatted_query = {}
    [formatted_query.update({item.id: schema.ShopUnit(**item)}) for item in query]

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
