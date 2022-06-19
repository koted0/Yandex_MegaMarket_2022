from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from .database import Base
import uuid


class ShopUnit(Base):
    __tablename__ = 'shop_unit'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    parentId = Column(UUID(as_uuid=True), ForeignKey(id), nullable=True)
    type = Column(Enum('OFFER', 'CATEGORY', name='shop_unit_type'), nullable=False)
    price = Column(Integer)
    children = relationship(
        "ShopUnit",
        # cascade deletions
        cascade="all, delete-orphan",
        # many to one + adjacency list - remote_side
        # is required to reference the 'remote'
        # column in the join condition.
        backref=backref("parent", remote_side=id),
        # children will be represented as a dictionary
        # on the "name" attribute.
        collection_class=attribute_mapped_collection("name"),
    )

    def __init__(self, id, name, price, date, type, parentId):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.price = price
        self.date = date
        self.type = type


