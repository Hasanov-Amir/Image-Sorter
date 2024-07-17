from ast import literal_eval
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.utils.color import yuv_distance
from app.controllers.sorting.serializer import SortingSerialzer
from app.controllers.image.serializer import ImageSerializer
from data.models import Image


class SortingAPI(Resource):
    serializer_class = SortingSerialzer

    def get_serializer(self):
        return self.serializer_class()
    
    def post(self):
        data = request.json
        serializer = self.get_serializer()
        image_serialzer = ImageSerializer()
        try:
            validated_data = serializer.load(data)
        except ValidationError as error:
            return {"error": error.messages}, 400
        
        sorted_images = []
        images = Image.filter()
        user_color = validated_data.get("color")
        for image in images:
            distance = yuv_distance(user_color, literal_eval(image.dominant_color))
            print(distance, image)
            if distance < 125:
                sorted_images.append(image)

        response = image_serialzer.dump(sorted_images, many=True)
        return response, 200
