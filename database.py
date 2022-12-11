from dotenv import load_dotenv
load_dotenv()

from app import app, db  # noqa
from app.models import Employee, Menu, MenuItem, MenuItemType, Order, Table  # noqa

with app.app_context():
    db.drop_all()
    db.create_all()

    # Seed employees
    cupcakke = Employee(
        name="Cupcakke", employee_number=69, password="yespapi")
    ternura = Employee(name="Ternura68", employee_number=68,
                       password="bendiciones")
    db.session.add(cupcakke)
    db.session.add(ternura)
    db.session.commit()

    # Seed menu item types
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")
    db.session.add(beverages)
    db.session.add(entrees)
    db.session.add(sides)
    db.session.commit()

    # Seed menus
    dinner = Menu(name="Dinner")
    db.session.add(dinner)
    db.session.commit()

    # Seed menu items
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98,
                         type=entrees, menu=dinner)
    db.session.add(fries)
    db.session.add(drp)
    db.session.add(jambalaya)
    db.session.commit()

    # Seed tables
    table1 = Table(number=1, capacity=4)
    table2 = Table(number=2, capacity=4)
    table3 = Table(number=3, capacity=4)
    table4 = Table(number=4, capacity=4)
    table5 = Table(number=5, capacity=6)
    table6 = Table(number=6, capacity=6)
    table7 = Table(number=7, capacity=6)
    table8 = Table(number=8, capacity=2)
    table9 = Table(number=9, capacity=2)
    table10 = Table(number=10, capacity=2)
    db.session.add(table1)
    db.session.add(table2)
    db.session.add(table3)
    db.session.add(table4)
    db.session.add(table5)
    db.session.add(table6)
    db.session.add(table7)
    db.session.add(table8)
    db.session.add(table9)
    db.session.add(table10)
    db.session.commit()

    # Seed orders
    order1 = Order(server_id=1, table_id=5, finished=False)
    order2 = Order(server_id=1, table_id=10, finished=True)
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()

    # Seed order details
    order1.items.append(fries)
    order1.items.append(drp)
    order2.items.append(fries)
    order2.items.append(drp)
    order2.items.append(jambalaya)

    db.session.commit()
