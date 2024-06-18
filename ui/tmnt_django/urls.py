from django.urls import path

from . import views

urlpatterns = [
    path("", views.test, name="test"),
    path("dfd_view/", views.upload_file, name="upload_file"),
    path("asset_view/", views.asset_viewer, name="asset_view"),
    path("api/add_actor", views.add_actor, name="add_actor"),
    path("api/add_boundary", views.add_boundary, name="add_boundary"),
    path("api/add_externalasset", views.add_externalasset, name="add_externalasset"),
]
