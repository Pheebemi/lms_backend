import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


def get_admin_notification_emails():
    """
    Who should be alerted about a new handoff.

    Uses settings.ADMIN_ALERT_EMAILS if set, otherwise every active superuser.
    DB-sourced on purpose — a hard-coded address goes stale silently; promoting
    a user to superuser starts the alerts.
    """
    configured = getattr(settings, 'ADMIN_ALERT_EMAILS', None)
    if configured:
        return list(configured)

    return list(
        User.objects.filter(is_superuser=True, is_active=True)
        .exclude(email='')
        .values_list('email', flat=True)
    )


def send_contact_admin_alert_email(contact):
    """
    Email admins that a person is waiting for a reply. Returns True/False.
    Never raises — a failed email must not block saving the contact.
    """
    recipients = get_admin_notification_emails()
    if not recipients:
        logger.warning('No admin notification emails configured; skipping alert for contact %s', contact.pk)
        return False

    source_label = contact.get_source_display()
    account_label = f'Logged in as {contact.user.email}' if contact.user_id else 'Not logged in'
    received_at = timezone.localtime(contact.created_at).strftime('%d %b %Y, %I:%M %p')

    try:
        admin_path = reverse('admin:support_contact_change', args=[contact.pk])
        admin_url = f"{settings.BASE_URL.rstrip('/')}{admin_path}"
    except Exception:
        admin_url = settings.BASE_URL

    context = {
        'name': contact.name,
        'email': contact.email,
        'message': contact.message,
        'conversation': contact.conversation,
        'source_label': source_label,
        'account_label': account_label,
        'received_at': received_at,
        'admin_url': admin_url,
    }

    subject = f'New message from {contact.name} ({source_label})'

    # Plain-text fallback (built here, not a template, so text-only clients read it)
    text_lines = [
        f'{contact.name} sent a message from {source_label} and is waiting for a reply.',
        '',
        f'Name:     {contact.name}',
        f'Email:    {contact.email}',
        f'Account:  {account_label}',
        f'Received: {received_at}',
        '',
        'Message:',
        contact.message,
    ]
    if contact.conversation:
        text_lines += ['', 'What they already asked the assistant:', contact.conversation]
    text_lines += ['', f'Open in admin: {admin_url}']
    text_body = '\n'.join(text_lines)

    try:
        html_body = render_to_string('support/email/contact_admin_alert.html', context)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=False)
        return True
    except Exception:
        logger.exception('Failed to send contact admin alert for contact %s', contact.pk)
        return False
