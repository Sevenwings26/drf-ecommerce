from django.contrib import admin

# Register your models here.
from .models import CustomUser, UserProfile, VendorProfile

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(VendorProfile)
