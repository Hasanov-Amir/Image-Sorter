from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.controllers.folder.serializers import FolderSerializer
from data.models import Folder


class FolderAPI(Resource):
    serializer_class = FolderSerializer

    def get_serializer(self):
        return self.serializer_class()

    @staticmethod
    def parse_created_to_http_code(created):
        if created:
            return 201
        return 200

    def get(self):
        folders = Folder.filter()
        serializer = self.get_serializer()
        response = serializer.dump(folders, many=True)
        return response, 200

    def post(self):
        data = request.json
        serializer = self.get_serializer()
        try:
            validated_data = serializer.load(data)
        except ValidationError as error:
            return {"error": error.messages}, 400
        folder, created = Folder.get_or_create(path=validated_data.get("path"))
        response = serializer.dump(folder)
        return response, self.parse_created_to_http_code(created)
