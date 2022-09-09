import dataclasses
import typing
import datetime


@dataclasses.dataclass
class Order:
    id: int
    order_number: int
    price_dollar: int
    delivery_date: datetime.date

    @classmethod
    def convert_row_for_obj(cls, row):
        if len(row) != 4:
            return None
        try:
            date = row[3]
            if isinstance(date, str):
                return cls(
                    int(row[0]),
                    int(row[1]),
                    int(row[2]),
                    datetime.datetime.strptime(row[3], "%d.%m.%Y").date(),
                )
            return cls(*row)
        except Exception as er:
            print("Проблема с ковертацией в обьект", er)
        return None


@dataclasses.dataclass
class Coord:
    date: list
    price: list

    @classmethod
    def convert_row_for_obj(cls, row):
        return cls(*row)


if __name__ == "__main__":
    row = ["50", "1426726", "1997", "20.05.2022"]
    order = Order.convert_row_for_obj(row)
    print(order.delivery_date)
