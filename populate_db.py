from sqlalchemy.orm import sessionmaker
from models import engine, Item

DBSession = sessionmaker(bind=engine)
DB = DBSession()

def main():
    item1 = Item(
    name='Apple Juice',
    description='A healthy fruit juice from apple',
    price=2.99,
    stock_qty=150
    )
    DB.add(item1)
    DB.commit()
    print('Item1 Added')

    item2 = Item(
    name='Akara Burger',
    description='A delicious bean snackgood for energy',
    price=1.99,
    stock_qty=150
    )
    DB.add(item2)
    DB.commit()
    print('Item2 Added')

    item3 = Item(
    name='Moi moi',
    description='A yummy food courtesy of beans',
    price=3.99,
    stock_qty=150
    )
    DB.add(item3)
    DB.commit()
    print('Item3 Added')


if __name__ == '__main__':
    main()