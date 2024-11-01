from rest_framework import serializers
from .models import CustomUser, UserProfile, VendorProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        # Create the user
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            user_class="B",  # Set to Class B for regular users
        )

        # Create UserProfile with additional fields
        UserProfile.objects.create(user=user, firstname=first_name, lastname=last_name)

        return user


class VendorRegistrationSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(write_only=True, required=True)
    business_address = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["business_name", "email", "password", "business_address"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        business_name = validated_data.pop("business_name")
        business_address = validated_data.pop("business_address")

        # Create the user
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            user_class="C",  # Set to Class C for vendors
        )

        # Create VendorProfile with additional fields
        VendorProfile.objects.create(
            user=user, business_name=business_name, business_address=business_address
        )

        return user
