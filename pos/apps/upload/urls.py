from django.urls import path
from . import views

app_name = "upload"
# api/v1/outlets/<path to view>/

urlpatterns = [
    path("file/", views.UploadFileAPIView.as_view(), name="upload_file"),
    path("files/", views.UploadFilesAPIView.as_view(), name="upload_files"),
    path("html/", views.UploadView.as_view(), name="html"),
]
