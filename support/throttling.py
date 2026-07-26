from rest_framework.throttling import SimpleRateThrottle


class SupportChatRateThrottle(SimpleRateThrottle):
    """Per-IP throttle for the AI chat endpoint — the only guard on the AI bill."""
    scope = 'support_chat'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),  # IP, even when authenticated
        }


class ContactRateThrottle(SimpleRateThrottle):
    """Per-IP throttle for the contact/handoff endpoint — stops inbox flooding."""
    scope = 'support_contact'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }
