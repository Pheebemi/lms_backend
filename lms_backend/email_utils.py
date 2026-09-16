"""
Two mailboxes, one SMTP host.

noreply@ is Django's default connection (settings.EMAIL_HOST_USER /
DEFAULT_FROM_EMAIL) — used automatically by any EmailMessage /
EmailMultiAlternatives sent with no explicit `connection=`. That's what
authentication/utils.py uses for OTP codes and password resets.

info@ is a second, explicitly-built connection for human-facing mail
(contact-form alerts, SIWES letters) — send_from_info() below.

Most SMTP hosts require the authenticated mailbox and the From address to
match, or the send is rejected or silently rewritten back to the login
address. So CONTACT_EMAIL and CONTACT_EMAIL_HOST_USER must always travel
together — never mix an info@ From address with the noreply@ connection
or vice versa.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

logger = logging.getLogger(__name__)


def get_contact_connection():
    """
    An SMTP connection authenticated as the info@ mailbox, or None if it
    hasn't been provisioned/configured yet (CONTACT_EMAIL_HOST_USER unset).
    """
    if not settings.CONTACT_EMAIL_HOST_USER:
        return None
    return get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.CONTACT_EMAIL_HOST_USER,
        password=settings.CONTACT_EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        use_ssl=settings.EMAIL_USE_SSL,
    )


def send_from_info(*, subject, text_body, to, html_body=None, reply_to=None,
                    attachments=None, fail_silently=True):
    """
    Send a human-facing email as the info@ mailbox.

    Falls back to the default (noreply@) connection and From address if
    info@ hasn't been configured yet, so call sites can be wired up to this
    before the second mailbox is provisioned without breaking anything.

    `attachments` is an iterable of (filename, content, mimetype) tuples,
    matching EmailMessage.attach()'s signature.
    """
    connection = get_contact_connection()
    from_email = settings.CONTACT_EMAIL if connection else settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to if isinstance(to, (list, tuple)) else [to],
        reply_to=[reply_to] if reply_to else None,
        connection=connection,
    )
    if html_body:
        msg.attach_alternative(html_body, 'text/html')
    for filename, content, mimetype in (attachments or []):
        msg.attach(filename, content, mimetype)

    try:
        msg.send(fail_silently=fail_silently)
        return True
    except Exception:
        if fail_silently:
            logger.exception('Failed to send info@ email: %s', subject)
            return False
        raise
