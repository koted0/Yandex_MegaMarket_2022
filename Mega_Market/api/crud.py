from datetime import datetime, timedelta
from pytz import UTC
from sqlalchemy import distinct

from . import schemas, models, shop_service, statistics_service
from uuid import UUID
from sqlalchemy.orm import Session


def _update_shop_unit(parentId: UUID, date: datetime, db: Session):
    parent = shop_service.find_unit(parentId, db)
    if not parent:
        return

    condition = {
        "OFFER": {'id': parentId},
        "CATEGORY": {'parentId': parentId}
    }

    # calc avg price of category
    avg_price = shop_service.find_avg(parentId, db)

    parent.price = avg_price
    parent.date = date

    statistics_service.post_statistics_to_db(parent.id, date, avg_price, db)

    db.commit()
    if parent.parentId is not None:
        _update_shop_unit(parent.parentId, date, db)


# main post method
def post_item_to_db(shop_unit_request: schemas.ShopUnitImportRequest, db: Session):
    for unit in shop_unit_request.items:
        shop_unit = shop_service.find_unit(unit.id, db)
        if not shop_unit:
            db.add(shop_service.make_models_from_schema(unit, shop_unit_request.updateDate))
        else:
            shop_unit.name = unit.name
            shop_unit.price = unit.price
            shop_unit.parentId = unit.parentId
            shop_unit.date = shop_unit_request.updateDate
        db.commit()
        _update_shop_unit(unit.id, shop_unit_request.updateDate, db)


# main delete method
def delete_item_from_db(shop_unit_id: UUID, db: Session):
    db.delete(shop_service.find_unit(shop_unit_id, db))
    db.commit()


# main get method
def get_item_from_db(shop_unit_id: UUID, db: Session):
    parents_tree = shop_service.get_parent_tree(shop_unit_id, db)
    return shop_service.map_shop_units_to_tree(parents_tree)


# main sales method
def get_sales_from_db(date: datetime, db: Session):
    """return all changed price row from statistics table in last 24 hours"""
    time_24_hours_ago = date - timedelta(hours=24)
    sales_in_24_hour = db.query(distinct(models.Statistics.id))\
        .filter(models.Statistics.date.between(time_24_hours_ago, date)).as_scalar()

    # return sales_in_24_hour
    return db.query(models.ShopUnit).filter(models.ShopUnit.id.in_(sales_in_24_hour)).all()
