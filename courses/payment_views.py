import requests
import uuid
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Course, Payment, Enrollment
from .payment_serializers import (
    PaymentSerializer, CreatePaymentSerializer, FlutterwavePaymentSerializer
)

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """
    Initiate Flutterwave payment for course purchase
    """
    serializer = CreatePaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    course_id = serializer.validated_data['course_id']
    amount = serializer.validated_data['amount']
    currency = serializer.validated_data['currency']
    
    try:
        course = Course.objects.get(id=course_id)
        student = request.user
        
        # Check if user is already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({
                'error': 'You are already enrolled in this course'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already has a pending payment for this course
        existing_payment = Payment.objects.filter(
            student=student,
            course=course,
            status='pending'
        ).first()
        
        if existing_payment:
            # Return the existing payment URL instead of creating a new one
            return Response({
                'message': 'You already have a pending payment for this course',
                'payment_url': f"{settings.FRONTEND_URL}/student/courses/{course_id}/payment-verify?tx_ref={existing_payment.flutterwave_reference}",
                'tx_ref': existing_payment.flutterwave_reference,
                'payment_id': str(existing_payment.id)
            }, status=status.HTTP_200_OK)
        
        # Create payment record
        payment = Payment.objects.create(
            student=student,
            course=course,
            amount=amount,
            currency=currency,
            status='pending'
        )
        
        # Generate Flutterwave payment data
        flutterwave_data = {
            'tx_ref': str(payment.id),
            'amount': payment.get_amount_in_kobo(),  # Convert to kobo
            'currency': currency,
            'redirect_url': f"{settings.FRONTEND_URL}/payment/callback",
            'customer': {
                'email': student.email,
                'name': student.full_name,
                'phone_number': student.phone_number or ''
            },
            'customizations': {
                'title': f"Payment for {course.title}",
                'description': f"Course: {course.title}",
                'logo': f"{settings.FRONTEND_URL}/logo.png"
            },
            'meta': {
                'course_id': str(course.id),
                'student_id': str(student.id),
                'payment_id': str(payment.id)
            }
        }
        
        # Make request to Flutterwave API
        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        print(f"🔑 Flutterwave Secret Key: {settings.FLUTTERWAVE_SECRET_KEY[:10]}...")
        print(f"📦 Flutterwave Data: {flutterwave_data}")
        
        try:
            response = requests.post(
                'https://api.flutterwave.com/v3/payments',
                json=flutterwave_data,
                headers=headers,
                timeout=30
            )
            
            print(f"📡 Flutterwave Response Status: {response.status_code}")
            print(f"📡 Flutterwave Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Flutterwave Request Error: {e}")
            payment.status = 'failed'
            payment.save()
            return Response({
                'error': 'Failed to connect to payment gateway',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                # Update payment with Flutterwave reference
                # Use the tx_ref as the reference since Flutterwave doesn't return a reference in the response
                payment.flutterwave_reference = flutterwave_data['tx_ref']
                payment.save()
                
                return Response({
                    'message': 'Payment initiated successfully',
                    'payment_id': str(payment.id),
                    'flutterwave_reference': payment.flutterwave_reference,
                    'payment_url': data['data']['link'],
                    'amount': float(amount),
                    'currency': currency,
                    'course_title': course.title
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to initiate payment',
                    'details': data.get('message', 'Unknown error')
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'Failed to connect to payment gateway',
                'details': response.text
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Course.DoesNotExist:
        return Response({
            'error': 'Course not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'An error occurred while initiating payment',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    """
    Verify Flutterwave payment and enroll user in course
    """
    serializer = FlutterwavePaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    tx_ref = serializer.validated_data['tx_ref']
    transaction_id = serializer.validated_data['transaction_id']
    status = serializer.validated_data['status']
    amount = serializer.validated_data['amount']
    
    try:
        # Get payment record
        payment = Payment.objects.get(
            id=tx_ref,
            student=request.user
        )
        
        # Verify with Flutterwave
        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success' and data['data']['status'] == 'successful':
                # Payment successful
                payment.status = 'completed'
                payment.flutterwave_transaction_id = transaction_id
                payment.paid_at = timezone.now()
                payment.metadata = data['data']
                payment.save()
                
                # Enroll user in course
                enrollment, created = Enrollment.objects.get_or_create(
                    student=request.user,
                    course=payment.course
                )
                
                if created:
                    # Update course student count
                    payment.course.total_students += 1
                    payment.course.save(update_fields=['total_students'])
                
                return Response({
                    'message': 'Payment verified successfully',
                    'enrollment_created': created,
                    'course_title': payment.course.title,
                    'amount_paid': float(payment.amount),
                    'currency': payment.currency
                }, status=status.HTTP_200_OK)
            else:
                # Payment failed
                payment.status = 'failed'
                payment.save()
                
                return Response({
                    'error': 'Payment verification failed',
                    'details': data.get('message', 'Payment was not successful')
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'Failed to verify payment',
                'details': response.text
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Payment.DoesNotExist:
        return Response({
            'error': 'Payment not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'An error occurred while verifying payment',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """
    Get user's payment history
    """
    payments = Payment.objects.filter(student=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    
    return Response({
        'payments': serializer.data,
        'total': payments.count()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_status(request, payment_id):
    """
    Get payment status by ID
    """
    try:
        payment = Payment.objects.get(id=payment_id, student=request.user)
        serializer = PaymentSerializer(payment)
        
        return Response({
            'payment': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Payment.DoesNotExist:
        return Response({
            'error': 'Payment not found'
        }, status=status.HTTP_404_NOT_FOUND)
