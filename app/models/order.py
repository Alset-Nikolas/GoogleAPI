from models import OrederModel, session
from dataclass.order import Order
import typing
import datetime
from sheet.dollar_rate import get_dollar_rate
from sqlalchemy import func
from dataclass.order import Order

DOLLAR_ROTATE = get_dollar_rate()


def get_expired_orders():
    global DOLLAR_ROTATE
    DOLLAR_ROTATE = get_dollar_rate()
    return (
        session.query(OrederModel)
        .filter(OrederModel.delivery_date < datetime.date.today())
        .all()
    )


def delete_orders_besides_ids(ids):
    session.query(OrederModel).filter(OrederModel.id.not_in(ids)).delete()


def update_all_orders(orders):
    ids = []
    for order_row in orders:
        order_valid = Order.convert_row_for_obj(order_row)
        if order_valid:
            id_ = int(order_row[0])
            ids.append(id_)
            check_to_update_order(order_valid)
    delete_orders_besides_ids(ids)
    session.commit()


def add_order(order: Order):
    new_order = OrederModel(
        id=order.id,
        order_number=order.order_number,
        price_dollar=order.price_dollar,
        price_rub=DOLLAR_ROTATE * order.price_dollar,
        delivery_date=order.delivery_date,
    )
    session.add(new_order)


def update_order(order_db: OrederModel, order: Order):
    # todo узнать цену рубля
    order_db.order_number = order.order_number
    order_db.price_dollar = order.price_dollar
    order_db.price_rub = DOLLAR_ROTATE * order.price_dollar
    order_db.delivery_date = order.delivery_date
    session.add(order_db)


def check_to_update_order(order: Order):
    order_db = session.query(OrederModel).filter(OrederModel.id == order.id).first()
    if not order_db:
        add_order(order)
        return
    update_order(order_db, order)


def get_coords_graf():
    coords = (
        session.query(
            OrederModel.delivery_date,
            func.sum(OrederModel.price_dollar).label("total_price"),
        )
        .group_by(OrederModel.delivery_date)
        .order_by(OrederModel.delivery_date)
        .all()
    )
    n = len(coords)
    dates = [0] * n
    prices = [0] * n
    for i in range(n):
        dates[i] = str(coords[i][0])
        prices[i] = int(coords[i][1])
    return dates, prices


def get_info_table():
    orders = (
        session.query(
            OrederModel.id,
            OrederModel.order_number,
            OrederModel.price_dollar,
            OrederModel.delivery_date,
        )
        .order_by(OrederModel.id)
        .all()
    )

    return [Order.convert_row_for_obj(order) for order in orders]


def get_total():
    return session.query(func.sum(OrederModel.price_dollar)).all()[0]
