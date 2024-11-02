from django.urls import path, include
from rest_framework.routers import DefaultRouter

# documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegistrationView,
    VendorRegistrationView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

router = DefaultRouter()
# router.register(r"user/resiger", UserRegistrationView, basename="user")
# router.register(r"vendor/register/", VendorRegistrationView, basename="vendors")

urlpatterns = [
    # swagger view
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    # sign-up
    path("", include(router.urls)),
    # product app
    path("product/", include("product.urls")),
    # token
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # # accounts
    path("user/register/", UserRegistrationView.as_view(), name="user"),
    path("vendor/register/", VendorRegistrationView.as_view(), name="vendor"),
    # password
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
