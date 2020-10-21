from django.urls import path, re_path
from .views import file_download
from django.conf.urls import url
urlpatterns = [
    re_path(r'^download/(?P<file_path>.*)/$', file_download, name='file_download'),
]
