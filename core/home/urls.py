from django.urls import path
from .views import home_view, MaterialDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^material/(?P<pk>\d+)$', MaterialDetailView.as_view(), name='material-detail'),

]
