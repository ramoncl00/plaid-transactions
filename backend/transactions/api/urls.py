from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.auth_view import AuthView
from api.views.link_token_views import LinkTokenView


urlpatterns = [
    path(r'auth/login', TokenObtainPairView.as_view(), name='auth'),
    path(r'auth/refresh', TokenRefreshView.as_view(), name='refresh'),
    path(r'auth/register', AuthView.as_view(), name='register'),
    path(r"link-token", LinkTokenView.as_view(), name='link-token')
]