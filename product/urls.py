from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryView, BrandView, ProductView

# documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"category", CategoryView, basename="category")
router.register(r"brand", BrandView, basename="brand")
router.register(r"product", ProductView, basename='product')

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
