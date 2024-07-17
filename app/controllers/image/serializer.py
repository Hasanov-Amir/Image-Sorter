from marshmallow import fields

from core.extensions import ma


class ImageSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    filename = fields.Str()
    folder_id = fields.UUID()
    dominant_color = fields.Str()
    orientation = fields.Str()
    favourite = fields.Bool()
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
