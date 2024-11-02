from rest_framework import generics, permissions
from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

# for documentation
from drf_spectacular.utils import extend_schema

# model and serializers
from .serializers import (
    ProductSerializer,
    ProductManagementSerializer,
    OrderManagementSerializer,
    UserManagementSerializer,
    VendorManagementSerializer,
    StaffManagementSerializer,
)
from account.models import CustomUser
from .models import Product, Order


# post product
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Customize with IsVendor if needed

    @extend_schema(responses=ProductSerializer)
    def perform_create(self, serializer):
        if self.request.user.user_class == "C":  # Ensure only vendors can create
            serializer.save(vendor=self.request.user)
        else:
            raise PermissionError("Only vendors can upload products.")


# Product List View
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_class == "C":  # Vendor
            return Product.objects.filter(vendor=self.request.user)
        elif self.request.user.user_class == "A":  # Admin
            return Product.objects.all()  # Admins can view all products
        else:
            raise PermissionDenied("You do not have permission to view products.")


# Product Detail View
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_class == "C":
            return Product.objects.filter(vendor=self.request.user)
        elif self.request.user.user_class == "A":
            return Product.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this product.")


# Product Update View
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if (
            self.request.user.user_class == "C"
            and serializer.instance.vendor == self.request.user
        ):
            serializer.save()
        else:
            raise PermissionDenied("You can only update your own products.")


# Product Delete View
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.user_class == "C" and instance.vendor == self.request.user:
            instance.delete()
        elif self.request.user.user_class == "A":  # Admin can delete any product
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this product.")


"""
    ADMIN DASHBOARD 
"""


class ProductManagementView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductManagementSerializer


class OrderManagementView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderManagementSerializer


class UserManagementView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_class="B")
    serializer_class = UserManagementSerializer


class VendorManagementView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_class="C")
    serializer_class = VendorManagementSerializer


class StaffManagementView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_staff=True)
    serializer_class = StaffManagementSerializer


"""
    VENDOR DASHBOARD
"""


class VendorProductManagementView(generics.ListAPIView):
    serializer_class = ProductManagementSerializer

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user)


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_class == "C"
