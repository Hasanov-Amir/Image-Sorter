import math

from flask import request
from flask_restful import Resource

from app.controllers.image.serializer import ImageSerializer
from core.extensions import db
from data.models import Image


class ImageAPI(Resource):
    serializer_class = ImageSerializer
    max_per_page = 100

    def get_serializer(self):
        return self.serializer_class()

    def get(self):
        args = request.args

        try:
            page = int(args.get("page", 1))
            per_page = int(args.get("per_page", self.max_per_page))
        except ValueError:
            return {"error": "page params must be int."}, 400

        if per_page > self.max_per_page:
            return {
                "error": f"per_page param cannot be higher than {self.max_per_page}"
            }

        images = db.paginate(
            db.select(Image),
            page=page,
            per_page=per_page,
            max_per_page=self.max_per_page,
        )
        serializer = self.get_serializer()
        serialized_images = serializer.dump(images, many=True)
        response = {
            "current_page": images.page,
            "current_page_images_count": len(serialized_images),
            "has_next": images.has_next,
            "has_prev": images.has_prev,
            "total_pages": math.ceil(images.total / per_page),
            "total_images": images.total,
            "images_per_page": per_page,
            "images": serialized_images,
        }
        return response, 200
