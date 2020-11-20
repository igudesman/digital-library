"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

from home.views import home_view
from home.views import my_logout
from moderator.views import moder_view
from registration.views import signup_view
from upload import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('upload/', views.upload, name='upload'),
    path('signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', include('registration.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('material/', include('search.urls')),
    path('moder/', moder_view, name="moder"),
    path('logout/', my_logout, name='my_logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
