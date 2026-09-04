"""
Emailing a generated SIWES letter to its recipient.

Follows the same shape as authentication/utils.py:send_otp_email — a branded
HTML email with a plain-text fallback, sent via DEFAULT_FROM_EMAIL. Unlike
that function this one does not swallow the exception: the OTP email is a
background nicety the user never sees fail, but here a management user is
directly asking "send this to the university" and needs to know if it did not
go out, rather than seeing a false success.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
]


def default_subject(letter) -> str:
    return f'SIWES Acceptance Letter — {letter.student_name} — ALGADDAF Technology Hub'


def default_message(letter) -> str:
    end_month, end_year = letter.end_month_year
    period = (
        f'{MONTH_NAMES[letter.start_month - 1]} {letter.start_year} '
        f'to {MONTH_NAMES[end_month - 1]} {end_year}'
    )
    return (
        f'Dear Sir/Ma,\n\n'
        f'Please find attached the SIWES acceptance letter for {letter.student_name} '
        f'({letter.registration_no}), accepted for industrial attachment with '
        f'ALGADDAF Technology Hub from {period}.\n\n'
        f'Kind regards,\nALGADDAF Technology Hub'
    )


def send_siwes_letter_email(*, letter, recipient_email, subject, message, pdf_bytes, filename):
    """
    Send the letter as a PDF attachment. Raises on failure rather than
    returning False, so the view can surface the actual error to the caller.
    """
    message_paragraphs = [p for p in message.split('\n\n') if p.strip()]

    html_body = render_to_string('management/email/siwes_letter_email.html', {
        'message_paragraphs': message_paragraphs,
        'student_name': letter.student_name,
        'reference_id': letter.reference_id,
    })

    msg = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.attach(filename, pdf_bytes, 'application/pdf')
    msg.send(fail_silently=False)
