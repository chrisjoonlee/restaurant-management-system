from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload

from app.forms.table_assignment import TableAssignmentForm
from app.models import db, Employee, MenuItem, MenuItemType, Order, Table

bp = Blueprint("orders", __name__, url_prefix="")


def calculate_total(order):
    print(order)


@bp.route("/")
@login_required
def index():
    # Data
    open_tables = Table \
        .query \
        .outerjoin(Order) \
        .filter(or_(Table.orders == None, Order.finished == True)) \
        .order_by(Table.number) \
        .all()
    servers = Employee.query.all()
    orders = Order \
        .query \
        .options(joinedload(Order.items)) \
        .filter(Order.server_id == current_user.id, Order.finished == False) \
        .all()
    menu_item_types = MenuItemType \
        .query \
        .join(MenuItem) \
        .order_by(MenuItemType.id, MenuItem.name) \
        .all()

    orders_and_total_prices = []
    for order in orders:
        total_price = sum([item.price for item in order.items])
        total_price = f"${total_price:.2f}"
        orders_and_total_prices.append(
            (order, total_price))

    # Table Assignment Form
    table_assignment_form = TableAssignmentForm()
    table_assignment_form.tables.choices = [
        (table.id, f"Table {table.number}") for table in open_tables]
    table_assignment_form.servers.choices = [
        (server.id, server.name) for server in servers]

    return render_template("orders.html",
                           table_assignment_form=table_assignment_form,
                           menu_item_types=menu_item_types,
                           tables=open_tables,
                           servers=servers,
                           orders_and_total_prices=orders_and_total_prices)


# Route for assigning tables
@ bp.route("/orders", methods=["POST"])
@ login_required
def assign_table():
    form_data = dict(request.form)
    order = Order(server_id=form_data['servers'],
                  table_id=form_data['tables'])
    db.session.add(order)
    db.session.commit()
    return redirect(url_for(".index"))


# Route for closing an order/table
@ bp.route("/orders/<int:id>/close", methods=["POST"])
@ login_required
def close_table(id):
    order = Order.query.get(id)
    order.finished = True
    print(order.finished)
    db.session.commit()
    return redirect(url_for(".index"))


# Route for adding to an order
@ bp.route("/orders/<int:id>/items", methods=["POST"])
@ login_required
def add_to_order(id):
    order = Order.query.get(id)
    form_data = dict(request.form)
    for entry in form_data:
        item_id = form_data[entry]
        item = MenuItem.query.get(item_id)
        order.items.append(item)
    db.session.commit()
    return redirect(url_for(".index"))
