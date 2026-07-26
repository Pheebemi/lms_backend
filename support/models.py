from django.db import models
from django.conf import settings


class Contact(models.Model):
    """
    A human-handoff message: someone who asked to talk to a person, either from
    the AI chat ("Talk to a human") or a plain contact form. This is the ONLY
    thing the support feature persists — chat conversations are never stored.
    """

    SOURCE_CHOICES = [
        ('chat', 'AI Chat'),
        ('contact_form', 'Contact Form'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='contact_form')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_index=True)

    # Chat transcript leading up to the handoff (empty for a plain contact form)
    conversation = models.TextField(blank=True, default='')

    # Set only if the sender happened to be logged in
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='support_contacts',
    )

    admin_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'support_contacts'
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"{self.name} <{self.email}> ({self.get_source_display()})"

    @property
    def short_message(self):
        return (self.message[:60] + '…') if len(self.message) > 60 else self.message
