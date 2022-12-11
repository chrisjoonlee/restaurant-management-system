from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


order_details = db.Table(
    "order_details",
    db.Model.metadata,
    db.Column("order_id",
              db.ForeignKey("orders.id"),
              primary_key=True,
              nullable=False),
    db.Column("menu_item.id",
              db.ForeignKey("menu_items.id"),
              primary_key=True,
              nullable=False)
)


class Employee(db.Model, UserMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    orders = db.relationship(
        "Order", back_populates="server", cascade="all, delete-orphan")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    items = db.relationship(
        "MenuItem", back_populates="menu", cascade="all, delete-orphan")


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey(
        "menus.id"), nullable=False)
    menu_type_id = db.Column(db.Integer, db.ForeignKey(
        "menu_item_types.id"), nullable=False)

    menu = db.relationship("Menu", back_populates="items")
    type = db.relationship("MenuItemType", back_populates="items")
    orders = db.relationship(
        "Order", secondary=order_details, back_populates="items")


class MenuItemType(db.Model):
    __tablename__ = "menu_item_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    items = db.relationship(
        "MenuItem", back_populates="type", cascade="all, delete-orphan")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey(
        "employees.id"), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey(
        "tables.id"), nullable=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)

    server = db.relationship("Employee", back_populates="orders")
    table = db.relationship("Table", back_populates="orders")
    items = db.relationship(
        "MenuItem", secondary=order_details, back_populates="orders")


class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

    orders = db.relationship(
        "Order", back_populates="table", cascade="all, delete-orphan")
