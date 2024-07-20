import math
from ast import literal_eval

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.controllers.image.serializer import ImageSerializer
from app.controllers.sorting.serializer import SortingSerialzer
from app.utils.color import yuv_distance
from data.models import Image


class SortingAPI(Resource):
    serializer_class = SortingSerialzer
    max_per_page = 100

    def get_serializer(self):
        return self.serializer_class()

    def get_sorted_images(self, images, validated_data):
        sorted_images = []
        user_color = validated_data.get("color")
        for image in images:
            distance = yuv_distance(user_color, literal_eval(image.dominant_color))
            if distance < 125:
                sorted_images.append(image)
        return sorted_images
    
    def paginate(self, images, page_size, page):
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return images[start_index:end_index]

    def post(self):
        data = request.json
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

            

        serializer = self.get_serializer()
        image_serialzer = ImageSerializer()
        try:
            validated_data = serializer.load(data)
        except ValidationError as error:
            return {"error": error.messages}, 400

        if orientation:=args.get("orientation", False):
            images = Image.filter(orientation=orientation)
        else:
            images = Image.filter()
        sorted_images = self.get_sorted_images(images, validated_data)
        serialized_images = image_serialzer.dump(
            sorted_images, many=True
        )
        paginated_images = self.paginate(serialized_images, per_page, page)
        total_pages = math.ceil(len(serialized_images) / per_page)
        response = {
            "current_page": page,
            "current_page_images_count": len(paginated_images),
            "has_next": page < total_pages,
            "has_prev": page != 1,
            "total_pages": total_pages,
            "total_images": len(serialized_images),
            "images_per_page": per_page,
            "images": paginated_images,
        }
        return response, 200
