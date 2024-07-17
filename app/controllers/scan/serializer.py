from marshmallow import fields

from core.extensions import ma


class ScanSerializer(ma.Schema):
    folder = fields.UUID(required=True)
