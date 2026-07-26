import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

OTP_EXPIRY_MINUTES = 10


def send_otp_email(email, otp_code, first_name='', is_resend=False):
    """
    Send the branded OTP verification email (HTML + plain-text fallback).
    Returns True on success, False on failure. Never raises.
    """
    subject = (
        'New verification code - Algaddaf Technology Hub'
        if is_resend else
        'Verify your email - Algaddaf Technology Hub'
    )

    context = {
        'first_name': first_name,
        'otp_code': otp_code,
        'is_resend': is_resend,
        'expiry_minutes': OTP_EXPIRY_MINUTES,
    }

    intro = (
        "Here's your new verification code for your Algaddaf Technology Hub account."
        if is_resend else
        'Thanks for signing up. Use the code below to verify your email address.'
    )
    text_body = (
        f"Hi{(' ' + first_name) if first_name else ''},\n\n"
        f"{intro}\n\n"
        f"Verification code: {otp_code}\n\n"
        f"This code expires in {OTP_EXPIRY_MINUTES} minutes. Please don't share it.\n\n"
        "If you didn't request this, you can ignore this email.\n\n"
        "Algaddaf Technology Hub"
    )

    try:
        html_body = render_to_string('authentication/email/otp_verification.html', context)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=False)
        return True
    except Exception:
        logger.exception('Failed to send OTP email to %s', email)
        return False
