"""
Emailing generated SIWES letters and manually issued certificates.

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


def default_certificate_subject(certificate) -> str:
    return f'Your Certificate — {certificate.course.name} — ALGADDAF Technology Hub'


def default_certificate_message(certificate) -> str:
    grade = certificate.get_grade_display()
    grade_clause = f' with a grade of {grade}' if grade else ''
    return (
        f'Dear {certificate.recipient_name},\n\n'
        f'Congratulations! Please find attached your certificate for '
        f'{certificate.course.name}{grade_clause} at ALGADDAF Technology Hub.\n\n'
        f'Kind regards,\nALGADDAF Technology Hub'
    )


def send_certificate_email(*, certificate, recipient_email, subject, message, png_bytes, filename):
    """
    Send a manually issued certificate as a PNG attachment. Raises on failure
    for the same reason send_siwes_letter_email does: a management user is
    directly asking for this to go out and must not see a false success.
    """
    message_paragraphs = [p for p in message.split('\n\n') if p.strip()]

    html_body = render_to_string('management/email/certificate_email.html', {
        'message_paragraphs': message_paragraphs,
        'recipient_name': certificate.recipient_name,
        'course_name': certificate.course.name,
        'certificate_id': certificate.certificate_id,
    })

    send_from_info(
        subject=subject,
        text_body=message,
        html_body=html_body,
        to=recipient_email,
        attachments=[(filename, png_bytes, 'image/png')],
        fail_silently=False,
    )
