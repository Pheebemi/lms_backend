import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

OTP_EXPIRY_MINUTES = 10
PASSWORD_RESET_EXPIRY_MINUTES = 10


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


def send_password_reset_email(email, otp_code, first_name=''):
    """
    Send the branded password-reset code email. Returns True on success,
    False on failure. Never raises.

    Must never raise or let its result change the caller's response: the
    request view always replies with the same generic message whether or
    not the account exists, so a distinguishable failure here (a bad
    address vs. a real send error) would leak account existence just as
    surely as a different HTTP status would.
    """
    subject = 'Reset your password - Algaddaf Technology Hub'

    context = {
        'first_name': first_name,
        'otp_code': otp_code,
        'expiry_minutes': PASSWORD_RESET_EXPIRY_MINUTES,
    }

    text_body = (
        f"Hi{(' ' + first_name) if first_name else ''},\n\n"
        "We received a request to reset your Algaddaf Technology Hub password.\n\n"
        f"Reset code: {otp_code}\n\n"
        f"This code expires in {PASSWORD_RESET_EXPIRY_MINUTES} minutes. Please don't share it.\n\n"
        "If you didn't request this, you can ignore this email — your password will not be changed.\n\n"
        "Algaddaf Technology Hub"
    )

    try:
        html_body = render_to_string('authentication/email/password_reset.html', context)
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
        logger.exception('Failed to send password reset email to %s', email)
        return False
