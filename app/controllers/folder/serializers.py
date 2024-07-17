from marshmallow import fields

from core.extensions import ma


class FolderSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    path = fields.Str(required=True)
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
