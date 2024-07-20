import os
from multiprocessing import Pool

from flask import current_app, request
from flask_restful import Resource
from marshmallow import ValidationError
from PIL import Image as pil_image
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.scan.serializer import ScanSerializer
from app.utils.dominant import get_dominant_color, get_image_orientation
from data.models import Folder, Image, db


class ScanAPI(Resource):
    serializer_class = ScanSerializer

    def get_serializer(self):
        return self.serializer_class()

    def get(self):
        data = request.args
        serializer = self.get_serializer()

        try:
            validated_data = serializer.load(data)
        except ValidationError as error:
            return {"error": error.messages}, 400

        self.folder_id = validated_data.get("folder")
        folder = Folder.get(self.folder_id)
        folder_path = folder.path

        try:
            self.run_scan(folder_path)
        except Exception as error:
            return {"error": str(error)}, 400

        return {}, 200

    def save_to_db_bulk(self, images_data):
        try:
            db.session.bulk_insert_mappings(Image, images_data)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def process_file(self, file_path):
        from core.factories import create_app

        app = create_app(prevent_overwrite=True)

        with app.app_context():
            filename = file_path.split(os.sep)[-1]
            image = pil_image.open(file_path).convert("RGB")
            dominant_color = get_dominant_color(image)
            orientation = get_image_orientation(image)
            print(file_path, dominant_color, orientation)

            return {
                "filename": filename,
                "folder_id": self.folder_id,
                "dominant_color": dominant_color,
                "orientation": orientation,
                "favourite": False,
            }

    def run_scan(self, folder_path):
        valid_files = []
        allowed_extensions = current_app.config.get("ALLOWED_EXTENSIONS")

        for filename in os.listdir(folder_path):
            if filename.split(".")[-1].lower() in allowed_extensions:
                valid_files.append(os.path.join(folder_path, filename))

        num_workers = max(1, os.cpu_count() - 2)

        with Pool(processes=num_workers) as pool:
            results = pool.map(self.process_file, valid_files)

        images = Image.filter(folder_id=self.folder_id)
        existing_images_filename = [image.filename for image in images]

        images_data = [
            result
            for result in results
            if result.get("filename") not in existing_images_filename
        ]
        self.save_to_db_bulk(images_data)
