from sqlalchemy.orm import sessionmaker
from models import engine, StockItem

DBSession = sessionmaker(bind=engine)
DB = DBSession()

def main():
    StockItem1 = StockItem(
    name='Apple Juice',
    description='A healthy fruit juice from apple',
    price=2.99,
    stock_qty=150
    )
    DB.add(StockItem1)
    DB.commit()
    print('StockItem1 Added')

    StockItem2 = StockItem(
    name='Akara Burger',
    description='A delicious bean snackgood for energy',
    price=1.99,
    stock_qty=150
    )
    DB.add(StockItem2)
    DB.commit()
    print('StockItem2 Added')

    StockItem3 = StockItem(
    name='Moi moi',
    description='A yummy food courtesy of beans',
    price=3.99,
    stock_qty=150
    )
    DB.add(StockItem3)
    DB.commit()
    print('StockItem3 Added')


if __name__ == '__main__':
    main()