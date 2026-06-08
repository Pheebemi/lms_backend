from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'


class RegisterRateThrottle(AnonRateThrottle):
    scope = 'register'


class OTPVerifyRateThrottle(AnonRateThrottle):
    scope = 'otp_verify'


class OTPResendRateThrottle(AnonRateThrottle):
    scope = 'otp_resend'
