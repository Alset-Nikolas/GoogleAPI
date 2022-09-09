from flask import Flask
from models.order import get_coords_graf, get_info_table, get_total
from server.schemas import CoordsSchema, TableSchema, TotalSchema
import typing

app = Flask(__name__)


@app.route("/grafic")
def grafic():
    schema = CoordsSchema()
    date, price = get_coords_graf()
    result = schema.load({"date": date, "price": price})
    return schema.dump(result)


@app.route("/table")
def table():
    schema = TableSchema()
    table_info = get_info_table()
    return schema.dump(table_info, many=True)


@app.route("/total")
def total():
    schema = TotalSchema()
    total = get_total()
    return schema.dump({"total": total[0]})


if __name__ == "__main__":
    app.run(debug=True)
