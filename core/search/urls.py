from django.urls import path, re_path
from .views import file_download
from .views import material_page
from django.conf.urls import url
urlpatterns = [
	path('material/<int:material_id>/', material_page, name='material'),
    re_path(r'^download/(?P<file_path>.*)/$', file_download, name='file_download'),
]
