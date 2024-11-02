from rest_framework import serializers
from .models import Product, Order
from account.models import CustomUser


class ProductSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(
        source="vendor.vendorprofile.business_name", read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "business_name",
        ]


class ProductManagementSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(
        source="vendor.vendorprofile.business_name", read_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "image", "name", "category", "stock", "sold", "vendor_name"]


class OrderManagementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    customer_name = serializers.CharField(
        source="customer.userprofile.firstname", read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "order_id",
            "product_name",
            "price",
            "customer_name",
            "address",
            "email",
            "date",
            "status",
        ]


class UserManagementSerializer(serializers.ModelSerializer):
    total_items_bought = serializers.SerializerMethodField()
    last_ordered = serializers.DateTimeField(
        source="customer_orders.latest.date", read_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "userprofile.firstname",
            "userprofile.lastname",
            "email",
            "address",
            "total_items_bought",
            "last_ordered",
        ]

    def get_total_items_bought(self, obj):
        return obj.customer_orders.count()


class VendorManagementSerializer(serializers.ModelSerializer):
    total_products = serializers.IntegerField(
        source="vendor_products.count", read_only=True
    )
    total_revenue = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "vendorprofile.business_name",
            "total_products",
            "date_joined",
            "total_revenue",
            "status",
        ]

    def get_total_revenue(self, obj):
        orders = obj.vendor_products.prefetch_related("orders")
        return sum(
            order.price * order.quantity
            for order in orders
            if order.status == "Delivered"
        )


class StaffManagementSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="staffprofile.role")
    status = serializers.CharField(source="staffprofile.status")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "userprofile.firstname",
            "userprofile.lastname",
            "email",
            "role",
            "status",
        ]
