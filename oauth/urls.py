from django.urls import path

import oauth.views as oauth

app_name = 'oauth'

urlpatterns = [
    path('authorize/', oauth.do_authorize, name='authorize'),
    path('redirect/', oauth.oauth_redirect, name='redirect'),
    path('token/', oauth.give_token, name='token'),
    path('error/', oauth.has_error, name='error'),
]
