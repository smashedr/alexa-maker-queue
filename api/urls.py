from django.urls import path

import api.views as api

app_name = 'api'

urlpatterns = [
    path('', api.api_home, name='home'),
    path('alexa/', api.alexa_post, name='alexa'),
]
