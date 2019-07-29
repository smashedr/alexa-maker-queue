from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('home.urls')),
    path('favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon.ico'
    )),
    path('api/', include('api.urls')),
    path('oauth/', include('oauth.urls')),
    path('admin/', admin.site.urls, name='django_admin'),
]
