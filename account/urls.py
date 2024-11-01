from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, VendorRegistrationView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # accounts
    path("user/register/", UserRegistrationView.as_view(), name="user"),
    path("vendor/register/", VendorRegistrationView.as_view(), name="vendor"),
]
