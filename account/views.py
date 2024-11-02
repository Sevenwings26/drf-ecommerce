from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse

# for documentation
from drf_spectacular.utils import extend_schema

# model and serializers
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    VendorRegistrationSerializer,
    PasswordResetConfirmSerializer,
)

# sign-up verification mail
from .utils import send_verification_email
from django.conf import settings

# reset password
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from django.template.loader import render_to_string


# views
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

        # Send verification email
        send_verification_email(user)

        tokens = get_tokens_for_user(user)
        return Response({"user": response.data, "tokens": tokens})


class VendorRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = VendorRegistrationSerializer

    @extend_schema(responses=VendorRegistrationSerializer)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(email=response.data["email"])

        # Send verification email
        send_verification_email(user)

        tokens = get_tokens_for_user(user)
        return Response({"vendor": response.data, "tokens": tokens})


# reset password


User = get_user_model()


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{reverse('password-reset-confirm')}?uid={uid}&token={token}"
            full_link = f"https://deployment.com{reset_link}"

            # Render the email template or use a simple message
            html_message = render_to_string(
                "password_reset.html",
                {
                    "user": user,
                    "reset_link": full_link,
                },
            )

            send_mail(
                subject="Password Reset Request",
                message="Click the following link to reset your password.",  # Plain text fallback
                from_email="from@example.com",  # Replace with your "from" email address
                recipient_list=[email],
                fail_silently=False,
                html_message=html_message,
            )

            return Response(
                {"detail": "Password reset link sent to your email."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PasswordResetConfirmView(generics.UpdateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User.objects.all()
