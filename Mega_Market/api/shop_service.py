from datetime import datetime
from typing import List, Tuple
from uuid import UUID

import pytz
from sqlalchemy.orm import Session
from . import models, schemas


def find_unit(unit_id: UUID, db: Session):
    return db.query(models.ShopUnit).filter_by(id=unit_id).first()


def make_models_from_schema(shop_unit: schemas.ShopUnitImport, date):
    return models.ShopUnit(**shop_unit.dict(), date=date)


def map_shop_units_to_tree(shop_units) -> models.ShopUnit:
    parents_tree = {}
    for item in shop_units:
        schema_item = schemas.ShopUnit.from_orm(item)
        schema_item.date = pytz.UTC.localize(schema_item.date)
        parents_tree[item.id] = schema_item

    root_unit = None

    # Part for parents and children
    for key, value in parents_tree.items():
        if value.parentId in parents_tree:
            if parents_tree[value.parentId].children is None:
                parents_tree[value.parentId].children = []
            parents_tree[value.parentId].children.append(value)
        else:
            root_unit = value

    return root_unit


def get_parent_tree(shop_unit_id: UUID, db: Session):
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


def find_avg(shop_unit_id: UUID, db: Session):
    return db.execute('WITH RECURSIVE category_path (id, price, type, "parentId") AS'
                      '('
                      'SELECT id, price, type, "parentId" '
                      'FROM shop_unit '
                      f"Where id = '{shop_unit_id}' "
                      'UNION ALL '
                      'SELECT c.id, c.price, c.type, c."parentId"'
                      'FROM category_path AS cp JOIN shop_unit AS c '
                      'ON cp.id = c."parentId") '
                      'SELECT avg(price) FROM category_path WHERE type != \'CATEGORY\' ').scalar()
