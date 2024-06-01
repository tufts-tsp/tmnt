from django.urls import path

from . import views

urlpatterns = [
    path("", views.test, name="test"),
    path("dfd_view/", views.upload_file, name="upload_file"),
    path("asset_view/", views.asset_viewer, name="asset_view"),
]
