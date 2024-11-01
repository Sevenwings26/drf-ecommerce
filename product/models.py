from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# # Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

#     class MPTTMeta:
#         order_insertion_by = ["name"]

#     def __str__(self):
#         return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE
    )  # delete product when brand is deleted...
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )  # When category is deleted, product will not be deleted...

    def __str__(self):
        return self.name
