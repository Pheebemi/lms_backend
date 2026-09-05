from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from .throttles import (
    LoginRateThrottle, RegisterRateThrottle, OTPVerifyRateThrottle, OTPResendRateThrottle,
    ForgotPasswordRateThrottle, ResetPasswordRateThrottle,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings
from .models import User, StudentProfile, TutorProfile, AdminProfile, EmailVerificationOTP, PasswordResetOTP
from .utils import send_otp_email, send_password_reset_email
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, ChangePasswordSerializer, OTPVerificationSerializer,
    ResendOTPSerializer, ForgotPasswordRequestSerializer, ResetPasswordConfirmSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterRateThrottle]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create role-specific profile
        if user.role == 'student':
            StudentProfile.objects.create(
                user=user,
                student_id=f"STU{user.id:06d}",
                enrollment_date=user.created_at.date()
            )
        elif user.role == 'tutor':
            TutorProfile.objects.create(
                user=user,
                employee_id=f"TUT{user.id:06d}",
                hire_date=user.created_at.date()
            )
        elif user.role == 'admin':
            AdminProfile.objects.create(
                user=user,
                employee_id=f"ADM{user.id:06d}",
                hire_date=user.created_at.date()
            )
        
        # Generate OTP for email verification
        otp = EmailVerificationOTP.generate_otp(user, user.email)
        
        # Send OTP via email
        send_otp_email(user.email, otp.otp_code, first_name=user.first_name)
        
        return Response({
            'message': 'User registered successfully. Please verify your email.',
            'user': UserSerializer(user).data,
            'email_verification_required': True,
            'email': user.email
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginRateThrottle])
def login_view(request):
    """
    User login endpoint
    """
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    
    # Check if email is verified
    if not user.is_verified:
        return Response({
            'error': 'Email not verified',
            'message': 'Please verify your email before signing in',
            'email': user.email,
            'verification_required': True
        }, status=status.HTTP_400_BAD_REQUEST)
    
    login(request, user)
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view - get and update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info_view(request):
    """
    Get current user information
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    Change user password
    """
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def role_based_users_view(request):
    """
    Get users based on role (admin only)
    """
    if not request.user.is_admin():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    role = request.GET.get('role')
    if role:
        users = User.objects.filter(role=role)
    else:
        users = User.objects.all()
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([OTPVerifyRateThrottle])
def verify_email_otp(request):
    """
    Verify email OTP
    """
    serializer = OTPVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    otp_code = serializer.validated_data['otp_code']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get the most recent valid OTP
    otp = EmailVerificationOTP.objects.filter(
        user=user, 
        email=email, 
        is_used=False
    ).order_by('-created_at').first()
    
    if not otp:
        return Response({
            'error': 'No valid OTP found. Please request a new one.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if otp.is_expired():
        return Response({
            'error': 'OTP has expired. Please request a new one.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if otp.attempts >= 3:
        return Response({
            'error': 'Too many failed attempts. Please request a new OTP.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if otp.verify(otp_code):
        # Generate JWT tokens after successful verification
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Email verified successfully!',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid OTP code',
            'attempts_remaining': 3 - otp.attempts - 1
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([OTPResendRateThrottle])
def resend_otp(request):
    """
    Resend OTP for email verification
    """
    serializer = ResendOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Return the same success response to prevent email enumeration
        return Response({
            'message': 'OTP sent successfully',
            'email': email
        }, status=status.HTTP_200_OK)

    if user.is_verified:
        return Response({
            'message': 'OTP sent successfully',
            'email': email
        }, status=status.HTTP_200_OK)
    
    # Generate new OTP
    otp = EmailVerificationOTP.generate_otp(user, email)
    
    # Send OTP via email
    send_otp_email(email, otp.otp_code, first_name=user.first_name, is_resend=True)
    
    return Response({
        'message': 'OTP sent successfully',
        'email': email
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([ForgotPasswordRateThrottle])
def forgot_password_request(request):
    """
    Request a password reset code.

    Always responds with the same generic message whether or not the
    account exists, and regardless of whether the email actually sent —
    a different response for either case would let the caller discover
    which email addresses have accounts.
    """
    serializer = ForgotPasswordRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email=email)
        otp = PasswordResetOTP.generate_otp(user, email)
        send_password_reset_email(email, otp.otp_code, first_name=user.first_name)
    except User.DoesNotExist:
        pass

    return Response({
        'message': 'If an account exists for this email, a reset code has been sent.',
        'email': email,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([ResetPasswordRateThrottle])
def forgot_password_confirm(request):
    """
    Verify the reset code and set the new password in the same step, so a
    code proves nothing on its own — it can only ever be spent together
    with an actual password change, never just "checked" and reused.
    """
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    # One generic error for "no such user", "no code", and "expired code" —
    # anything else would tell an attacker which emails have accounts.
    generic_error = {'error': 'Invalid or expired code. Please request a new one.'}

    try:
        user = User.objects.get(email=data['email'])
    except User.DoesNotExist:
        return Response(generic_error, status=status.HTTP_400_BAD_REQUEST)

    otp = PasswordResetOTP.objects.filter(
        user=user,
        email=data['email'],
        is_used=False
    ).order_by('-created_at').first()

    if not otp or otp.is_expired():
        return Response(generic_error, status=status.HTTP_400_BAD_REQUEST)

    if otp.attempts >= 3:
        return Response({
            'error': 'Too many incorrect attempts. Please request a new code.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if otp.otp_code != data['otp_code']:
        otp.attempts += 1
        otp.save(update_fields=['attempts'])
        return Response(generic_error, status=status.HTTP_400_BAD_REQUEST)

    otp.is_used = True
    otp.save(update_fields=['is_used'])
    # Any other outstanding codes for this user are now stale.
    PasswordResetOTP.objects.filter(user=user, is_used=False).exclude(pk=otp.pk).update(is_used=True)

    user.set_password(data['new_password'])
    user.save()

    return Response({
        'message': 'Password reset successfully. Please sign in with your new password.'
    }, status=status.HTTP_200_OK)
