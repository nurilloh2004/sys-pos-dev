from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from apps.core.services.generics import CustomAPIView, CustomGenericAPIView
# from apps.core.services.status import *
from django.views import View
from apps.core.services.generics import POSResponse
from . import serializers as ser
from apps.upload.models import UploadFile


class UploadFileAPIView(CustomGenericAPIView):
    """
    POST: http://127.0.0.1:8000/api/uploads/v1/upload-file
    """
    tags = ["Upload image"]
    serializer_class = ser.UploadFileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return self.success_response(results={"id": serializer.instance.id, "url": serializer.instance.url})
            else:
                self.code = POSResponse.CODE_3
                self.error_message = POSResponse.MSG_3
                return self.error_response()
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class UploadFilesAPIView(CustomAPIView):
    """
    POST: http://127.0.0.1:8585/api/v1/upload/files/
    """
    tags = ["Multiple Files Upload API"]
    serializer_class = ser.UploadFilesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = [{"file": item} for item in request.FILES.getlist('files', None)]
            if data:
                serializer = self.serializer_class(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return self.success_response(results=[{"id": obj.id, "url": obj.url} for obj in serializer.instance])
            else:
                self.update_error_text(catch="File")
                self.code = POSResponse.CODE_6
                self.error_message = POSResponse.MSG_6
                return self.error_response()
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()

    def delete(self, request):
        invalid_id = None
        try:
            for file_id in request.data['ids']:
                if not UploadFile.objects.filter(id=file_id).exists():
                    invalid_id = file_id
                    break

            if invalid_id:
                self.update_error_text(catch=invalid_id)
                self.code = POSResponse.CODE_4
                self.error_message = POSResponse.MSG_4
                return self.error_response()

            for file_id in request.data['ids']:

                UploadFile.objects.get(id=file_id).delete()
            return self.success_response()

        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class UploadView(View):

    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {})