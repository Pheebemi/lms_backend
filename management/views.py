from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import CourseCatalog, StudentRecord, ManualCertificate, SiwesLetter
from .serializers import (
    CourseCatalogSerializer,
    StudentRecordSerializer,
    StudentRecordListSerializer,
    ManualCertificateSerializer,
    SiwesLetterSerializer,
)


class IsManagementOrAdmin(permissions.BasePermission):
    """Allow access only to management or admin users."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('management', 'admin')
        )


# ── Course Catalog ──────────────────────────────────────────────────────────

class CourseCatalogListView(generics.ListAPIView):
    """List of active courses — used by the enrollment form dropdown."""
    serializer_class = CourseCatalogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseCatalog.objects.filter(is_active=True)


class CourseCatalogAdminListCreateView(generics.ListCreateAPIView):
    """All courses (including inactive) — management/admin only."""
    serializer_class = CourseCatalogSerializer
    permission_classes = [IsManagementOrAdmin]
    queryset = CourseCatalog.objects.all()


class CourseCatalogAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single course — management/admin only."""
    serializer_class = CourseCatalogSerializer
    permission_classes = [IsManagementOrAdmin]
    queryset = CourseCatalog.objects.all()


# ── Student Records ─────────────────────────────────────────────────────────

class StudentRecordListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManagementOrAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentRecordListSerializer
        return StudentRecordSerializer

    def get_queryset(self):
        qs = StudentRecord.objects.select_related('course', 'created_by').all()

        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(application_status=status_param)

        student_type = self.request.query_params.get('student_type')
        if student_type:
            qs = qs.filter(student_type=student_type)

        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_no__icontains=search) |
                Q(id_no__icontains=search)
            )

        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(created_at__year=year)
        if month:
            qs = qs.filter(created_at__month=month)

        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StudentRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManagementOrAdmin]
    serializer_class = StudentRecordSerializer
    queryset = StudentRecord.objects.select_related('course', 'created_by').all()
    lookup_field = 'pk'


class StudentRecordApproveView(APIView):
    """Quick approve / decline action."""
    permission_classes = [IsManagementOrAdmin]

    def patch(self, request, pk):
        record = get_object_or_404(StudentRecord, pk=pk)
        new_status = request.data.get('application_status')
        if new_status not in ('approved', 'declined', 'pending'):
            return Response(
                {'error': 'Invalid status. Use approved, declined, or pending.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record.application_status = new_status
        record.save(update_fields=['application_status', 'updated_at'])
        return Response({'id': str(record.id), 'application_status': record.application_status})


class ManualCertificateListView(generics.ListAPIView):
    """List previously generated manual certificates — management/admin only."""
    serializer_class = ManualCertificateSerializer
    permission_classes = [IsManagementOrAdmin]

    def get_queryset(self):
        qs = ManualCertificate.objects.select_related('course', 'created_by').all()
        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(recipient_name__icontains=search) |
                Q(certificate_id__icontains=search)
            )
        return qs


class GenerateManualCertificateView(APIView):
    """
    Manually issue a certificate from the management dashboard.

    Accepts a typed recipient name + a CourseCatalog course, generates (or reuses)
    a stable certificate ID for that recipient + course, renders the certificate
    PNG and returns it as a download. Regenerating for the same recipient + course
    always reuses the same certificate ID.
    """
    permission_classes = [IsManagementOrAdmin]

    def post(self, request):
        serializer = ManualCertificateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipient_name = serializer.validated_data['recipient_name']
        course = serializer.validated_data['course']
        grade = serializer.validated_data.get('grade', '')

        # Reuse an existing certificate for the same recipient + course so the ID
        # is stable across regenerations (case-insensitive name match).
        certificate = (
            ManualCertificate.objects
            .filter(recipient_name__iexact=recipient_name, course=course)
            .first()
        )
        if certificate is None:
            certificate = ManualCertificate.objects.create(
                recipient_name=recipient_name,
                course=course,
                grade=grade,
                created_by=request.user,
            )
        elif certificate.grade != grade:
            # Keep the same ID but allow the grade to be corrected
            certificate.grade = grade
            certificate.save(update_fields=['grade'])

        # Render the certificate PNG
        from courses.certificate_generator import generate_certificate_png

        img_buffer = generate_certificate_png(
            student_name=certificate.recipient_name,
            course_title=course.name,
            certificate_id=certificate.certificate_id,
            completed_date=certificate.issued_at,
            grade=certificate.grade,
        )

        response = HttpResponse(img_buffer.read(), content_type='image/png')
        safe_name = certificate.recipient_name.replace(' ', '_')
        response['Content-Disposition'] = (
            f'attachment; filename="certificate_{certificate.certificate_id}_{safe_name}.png"'
        )
        # Expose the ID to the browser fetch so the UI can display it
        response['X-Certificate-Id'] = certificate.certificate_id
        response['Access-Control-Expose-Headers'] = 'X-Certificate-Id, Content-Disposition'
        return response


class ManagementStatsView(APIView):
    """Summary stats for the management dashboard home."""
    permission_classes = [IsManagementOrAdmin]

    def get(self, request):
        from django.db.models import Sum

        qs = StudentRecord.objects.all()

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if year:
            qs = qs.filter(created_at__year=year)
        if month:
            qs = qs.filter(created_at__month=month)

        total = qs.count()
        pending = qs.filter(application_status='pending').count()
        approved = qs.filter(application_status='approved').count()
        declined = qs.filter(application_status='declined').count()

        totals = qs.aggregate(
            total_expected=Sum('amount_to_pay'),
            total_collected=Sum('amount_paid'),
            total_balance=Sum('balance'),
        )

        return Response({
            'students': {
                'total': total,
                'pending': pending,
                'approved': approved,
                'declined': declined,
            },
            'fees': {
                'total_expected': totals['total_expected'] or 0,
                'total_collected': totals['total_collected'] or 0,
                'total_balance': totals['total_balance'] or 0,
            },
            'filter': {'month': month, 'year': year},
        })


# ── SIWES acceptance letters ────────────────────────────────────────────────

class SiwesLetterListView(generics.ListAPIView):
    """List previously issued SIWES acceptance letters — management/admin only."""
    serializer_class = SiwesLetterSerializer
    permission_classes = [IsManagementOrAdmin]

    def get_queryset(self):
        qs = SiwesLetter.objects.select_related('created_by').all()
        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(student_name__icontains=search) |
                Q(registration_no__icontains=search) |
                Q(institution__icontains=search) |
                Q(reference_id__icontains=search)
            )
        return qs


class GenerateSiwesLetterView(APIView):
    """
    Render a SIWES acceptance letter as a PDF and stream it back.

    Saves the letter first so there is a record of what was issued, then returns
    the file bytes directly. The reference is echoed in a header so the browser
    can show it without a second request.

    Passing `letter_id` re-renders an existing letter, keeping its reference —
    that is what the Regenerate action in the history list sends.
    """
    permission_classes = [IsManagementOrAdmin]

    def post(self, request):
        letter_id = request.data.get('letter_id')
        if letter_id:
            letter = get_object_or_404(SiwesLetter, pk=letter_id)
        else:
            serializer = SiwesLetterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            letter = serializer.save(created_by=request.user)

        from .siwes_letter import generate_siwes_letter_pdf
        buf = generate_siwes_letter_pdf(
            student_name=letter.student_name,
            course_of_study=letter.course_of_study,
            registration_no=letter.registration_no,
            institution=letter.institution,
            institution_state=letter.institution_state,
            duration_months=letter.duration_months,
            start_month=letter.start_month,
            start_year=letter.start_year,
            letter_date=letter.letter_date,
        )

        response = HttpResponse(buf.read(), content_type='application/pdf')
        safe_name = ''.join(
            ch if ch.isalnum() else '_' for ch in letter.student_name
        ).strip('_')
        response['Content-Disposition'] = (
            f'attachment; filename="siwes_{letter.reference_id}_{safe_name}.pdf"'
        )
        response['X-Letter-Id'] = letter.reference_id
        response['Access-Control-Expose-Headers'] = 'X-Letter-Id, Content-Disposition'
        return response
