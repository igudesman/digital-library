from django.urls import path, re_path

from .views import file_download
from .views import material_page, change_view, delete_view

urlpatterns = [
    path('<int:material_id>/', material_page, name='material'),
    re_path(r'^download/(?P<file_path>.*)$', file_download, name='file_download'),
    path(r"delete/<int:material_id>/", delete_view, name="delete"),
    path(r"change_visibility/<int:material_id>/", change_view, name="change"),
]
