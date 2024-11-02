from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

# documentation
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
# router.register(r"upload_product", ProductCreateView, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    # path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    # """Product - CRUD """
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
]
