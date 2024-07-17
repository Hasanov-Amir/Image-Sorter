from marshmallow import fields

from core.extensions import ma


class SortingSerialzer(ma.Schema):
    color = fields.List(fields.Integer(), required=True)
