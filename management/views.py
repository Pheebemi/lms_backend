from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import CourseCatalog, StudentRecord
from .serializers import (
    CourseCatalogSerializer,
    StudentRecordSerializer,
    StudentRecordListSerializer,
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


class ManagementStatsView(APIView):
    """Summary stats for the management dashboard home."""
    permission_classes = [IsManagementOrAdmin]

    def get(self, request):
        from django.db.models import Sum

        total = StudentRecord.objects.count()
        pending = StudentRecord.objects.filter(application_status='pending').count()
        approved = StudentRecord.objects.filter(application_status='approved').count()
        declined = StudentRecord.objects.filter(application_status='declined').count()

        totals = StudentRecord.objects.aggregate(
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
        })
