from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"{reverse('verify')}?uid={uid}&token={token}"

    # FRONTENDurl = "https://deployment.com/"
    confirmation_link = f"https://deployment.com/{verification_link}"

    # Render the email template
    html_message = render_to_string(
        "confirmation_emai.html",
        {
            "user": user,
            "verification_link": confirmation_link,
        },
    )

    send_mail(
        subject="Verify your email",
        message="Confirm Your Registration",  # Plain text fallback
        from_email="from@example.com",  # Replace with your "from" email address
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message,  # Send the rendered HTML content
    )
