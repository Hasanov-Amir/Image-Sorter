from flask import Flask

from app.controllers import folder, image, scan, sorting
from core.extensions import api, db, ma, migrator
from data import models as _models  # noqa: F401

settings = {"default": "core.config.Config"}


def register_api_resources():
    api.add_resource(folder.FolderAPI, "/api/folder/")
    api.add_resource(scan.ScanAPI, "/api/scan/")
    api.add_resource(image.ImageAPI, "/api/image/")
    api.add_resource(sorting.SortingAPI, "/api/sort/")


def register_extensions(app):
    ma.init_app(app)
    db.init_app(app)
    migrator.init_app(app)
    api.init_app(app)


def create_app(setting="default", prevent_overwrite=False):
    app = Flask(__name__)
    app.config.from_object(settings.get(setting))
    if not prevent_overwrite:
        register_api_resources()
    register_extensions(app)
    return app
