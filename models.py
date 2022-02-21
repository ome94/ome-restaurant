import os

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(255), unique=True)
    password = Column(String(255))

class Item(Base):
    __tablename__ = "items"

    item_no = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    price = Column(Float)
    stock_qty = Column(Integer)

class Basket(Base):
    __tablename__ = "order_baskets"

    id = Column(Integer, primary_key=True)
    item_no = Column(Integer, ForeignKey('items.item_no'))
    user_id = Column(Integer, ForeignKey('users.id'))

class Order(Base):
    __tablename__ = "orders"

    order_no = Column(Integer, primary_key=True)
    order_time = Column(DateTime, default=datetime.isoformat(datetime.now()))
    basket = relationship(Basket)

# create DB engine
engine = create_engine(os.environ.get("DATABASE_URL"))

# create DB ORM Mapping
Base.metadata.create_all(engine)
