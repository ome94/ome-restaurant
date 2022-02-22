import os

from sqlalchemy import (create_engine,Boolean, ForeignKey,
    Column, Integer, String, Float)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(255), unique=True)
    password = Column(String(255))

class StockItem(Base):
    __tablename__ = "stock_items"

    item_no = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    price = Column(Float)
    stock_qty = Column(Integer)

class Selection(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True)
    item_no = Column(Integer, ForeignKey('stock_items.item_no'))
    user_id = Column(Integer, ForeignKey('users.id'))
    paid = Column(Boolean, default=False)
    item = relationship(StockItem)


# create DB engine
engine = create_engine(os.environ.get("DATABASE_URI"))

# create DB ORM Mapping
Base.metadata.create_all(engine)
