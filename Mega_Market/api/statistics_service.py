from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from . import models


def post_statistics_to_db(item_id: UUID, date: datetime, price: float, db: Session):
    db.execute(insert(models.Statistics).values(
        id=item_id,
        date=date,
        price=price
    ).on_conflict_do_update(constraint='statistics_pkey', set_=dict(price=price)))
    db.commit()
