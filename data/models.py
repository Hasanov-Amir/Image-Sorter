from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from data.base import Column, Model, db


class Image(Model):
    __tablename__ = "image"
    __table_args__ = (db.UniqueConstraint("filename", "folder_id"),)

    filename = Column("filename", String(300))
    folder_id = Column(UUID(as_uuid=True))
    dominant_color = Column("dominant_color", String(20))
    orientation = Column("orientation", String(20))
    favourite = Column("favourite", Boolean())

    def __init__(self, filename, folder_id, dominant_color, orientation, favourite):
        self.filename = filename
        self.folder_id = folder_id
        self.dominant_color = dominant_color
        self.orientation = orientation
        self.favourite = favourite

    def __str__(self):
        return f"<{self.id=}:{self.filename=}>"

    def __repr__(self):
        return f"<{self.id=}:{self.filename=}>"


class Folder(Model):
    __tablename__ = "folder"

    path = Column("path", String(200), unique=True)

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f"<{self.id=}:{self.path=}>"

    def __repr__(self):
        return f"<{self.id=}:{self.path=}>"
