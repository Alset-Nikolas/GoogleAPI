from marshmallow import Schema, fields


class CoordsSchema(Schema):
    date = fields.List(fields.String())
    price = fields.List(fields.Integer())


class TableSchema(Schema):
    id = fields.Integer()
    number_ofer = fields.Integer()
    price_dollar = fields.Integer()
    delivery_date = fields.Date()


class TotalSchema(Schema):
    total = fields.Integer()
