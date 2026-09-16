"""
Emailing a generated SIWES letter to its recipient.

Sent as info@ — a staff-signed notice to a university, not automated system
mail — via lms_backend/email_utils.py:send_from_info(). Unlike the OTP email
this one does not swallow the exception: the OTP email is a background
nicety the user never sees fail, but here a management user is directly
asking "send this to the university" and needs to know if it did not go
out, rather than seeing a false success.
"""
import logging

from django.template.loader import render_to_string

from lms_backend.email_utils import send_from_info

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

    send_from_info(
        subject=subject,
        text_body=message,
        html_body=html_body,
        to=recipient_email,
        attachments=[(filename, pdf_bytes, 'application/pdf')],
        fail_silently=False,
    )
