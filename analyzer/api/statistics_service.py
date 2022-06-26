from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import distinct
from . import models, schemas


def post_statistics_to_db(item_id: UUID, date: datetime, price: float, db: Session):
    db.execute(insert(models.Statistics).values(
        id=item_id,
        date=date,
        price=price
    ).on_conflict_do_update(constraint='statistics_pkey', set_=dict(price=price)))
    db.commit()


def find_statistic_in_24_hours(date_start: datetime, date_end: datetime, db: Session):
    return db.query(distinct(models.Statistics.id)) \
        .filter(models.Statistics.date.between(date_start, date_end)).as_scalar()


def find_in_interval(unit_id: UUID, date_start: datetime, date_end: datetime, db: Session):
    data = db.query(models.Statistics) \
        .filter_by(id=unit_id) \
        .filter(models.Statistics.date.between(date_start, date_end)).all()
    return data


def map_to_statistics(statistics, shop_unit) -> schemas.ShopUnitStatisticUnit:
    statistics_unit = schemas.ShopUnitStatisticUnit(
        id=statistics.id,
        name=shop_unit.name,
        price=statistics.price,
        date=statistics.date,
        type=shop_unit.type,
        parentId=shop_unit.parentId
    )

    return statistics_unit

