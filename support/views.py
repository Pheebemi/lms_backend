import logging

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .knowledge import build_system_prompt
from .serializers import ChatRequestSerializer, ContactSerializer
from .throttling import ContactRateThrottle, SupportChatRateThrottle
from .utils import send_contact_admin_alert_email

logger = logging.getLogger(__name__)

FRIENDLY_ERROR = (
    "Sorry, I'm having trouble right now. Please try again in a moment, or use "
    "the “Talk to a human” button below."
)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([SupportChatRateThrottle])
def support_chat(request):
    """
    Relay a client-held conversation to the AI provider and return one reply.
    Nothing is stored. The browser never sees the provider key.
    """
    # Key-gated: degrade gracefully to the contact option if unconfigured.
    if not settings.SUPPORT_AI_API_KEY:
        return Response(
            {'detail': 'The assistant is unavailable right now. Please use the contact option.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    serializer = ChatRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    messages = [{'role': 'system', 'content': build_system_prompt()}]
    messages += [
        {'role': m['role'], 'content': m['content']}
        for m in serializer.validated_data['messages']
    ]

    try:
        resp = requests.post(
            settings.SUPPORT_AI_API_URL,
            headers={
                'Authorization': f'Bearer {settings.SUPPORT_AI_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': settings.SUPPORT_AI_MODEL,
                'messages': messages,
                'temperature': 0.2,
                'max_tokens': 400,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data['choices'][0]['message']['content'].strip()
    except Exception:
        # Provider errors can leak billing/account detail — log, never surface.
        logger.exception('Support chat provider call failed')
        return Response({'reply': FRIENDLY_ERROR}, status=status.HTTP_200_OK)

    return Response({'reply': reply}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ContactRateThrottle])
def submit_contact(request):
    """
    Save a human-handoff message and email admins. Always returns 201 — the
    message is saved even if the email fails, so the sender is never told it
    failed (it's visible in admin regardless).
    """
    serializer = ContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user if request.user and request.user.is_authenticated else None
    contact = serializer.save(user=user)

    if send_contact_admin_alert_email(contact):
        contact.admin_notified = True
        contact.save(update_fields=['admin_notified'])

    return Response(
        {'success': True, 'message': "Thanks — we've got your message and will get back to you soon."},
        status=status.HTTP_201_CREATED,
    )
