from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# for documentation
from drf_spectacular.utils import extend_schema

# model and serializers
from .models import CustomUser
from .serializers import UserRegistrationSerializer, VendorRegistrationSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    @extend_schema(responses=UserRegistrationSerializer)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(email=response.data["email"])
        tokens = get_tokens_for_user(user)
        return Response({"user": response.data, "tokens": tokens})


class VendorRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = VendorRegistrationSerializer

    @extend_schema(responses=VendorRegistrationSerializer)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(email=response.data["email"])
        tokens = get_tokens_for_user(user)
        return Response({"vendor": response.data, "tokens": tokens})
