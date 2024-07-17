from flask_restful import Resource

from data.models import Image
from app.controllers.image.serializer import ImageSerializer


class ImageAPI(Resource):
    serializer_class = ImageSerializer

    def get_serializer(self):
        return self.serializer_class()

    def get(self):
        images = Image.filter()
        serializer = self.get_serializer()
        response = serializer.dump(images, many=True)
        return response, 200
