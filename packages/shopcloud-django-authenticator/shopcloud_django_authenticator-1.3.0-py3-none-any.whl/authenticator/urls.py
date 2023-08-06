from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()

urlpatterns = [
    path('login', views.login_view, name='authenticator-login'),
    path('login-credential-rotation', views.login_credential_rotation, name='authenticator-login-credential-rotation'),
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
