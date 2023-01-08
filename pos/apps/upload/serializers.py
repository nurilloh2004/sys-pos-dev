from rest_framework import serializers
from apps.upload.models import UploadFile


class UploadFilesSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = UploadFile
        fields = ('id', 'file')


class UploadFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadFile
        fields = ('id', 'file')
