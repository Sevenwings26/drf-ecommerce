from django.db import models
from django.utils.text import slugify

# from django.contrib.auth import get_user_model
from account.models import CustomUser
from account.models import (
    CustomUser,
)  # Adjust the import path as necessary

# User = get_user_model()


# Staff model
class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=[("Active", "Active"), ("Inactive", "Inactive")]
    )

    def __str__(self):
        return f"{self.user.email} - {self.role}"


# Class C (Vendors) should be filtered by their user type, and a related field can be used to assign products.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending Approval"),
        ("banned", "Banned"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True
    )
    vendor = models.ForeignKey(
        CustomUser, related_name="vendor_products", on_delete=models.CASCADE
    )

    admin_reviewed = models.BooleanField(
        default=False
    )  # Marks if the product has been reviewed by an admin

    def get_business_name(self):
        # Return the business name from the related VendorProfile
        if hasattr(self.vendor, "vendorprofile"):
            return self.vendor.vendorprofile.business_name
        return "N/A"

    def __str__(self):
        return f"{self.name} by {self.get_business_name()}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Inventory(models.Model):
    product = models.OneToOneField(
        Product, related_name="inventory", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    restock_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser, related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} on {self.product.name}"


# Consider permissions on views to distinguish between Admin (Class A), Users (Class B), and Vendors (Class C).


# order
class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        CustomUser, related_name="customer_orders", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
    )

    def __str__(self):
        return f"Order {self.order_id} - {self.product.name}"
