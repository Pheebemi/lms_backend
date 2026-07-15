from django.urls import path
from .views import (
    CourseCatalogListView,
    CourseCatalogAdminListCreateView,
    CourseCatalogAdminDetailView,
    StudentRecordListCreateView,
    StudentRecordDetailView,
    StudentRecordApproveView,
    ManualCertificateListView,
    GenerateManualCertificateView,
    ManagementStatsView,
)

urlpatterns = [
    path('courses/', CourseCatalogListView.as_view(), name='course-catalog-list'),
    path('courses/admin/', CourseCatalogAdminListCreateView.as_view(), name='course-catalog-admin'),
    path('courses/admin/<int:pk>/', CourseCatalogAdminDetailView.as_view(), name='course-catalog-admin-detail'),
    path('records/', StudentRecordListCreateView.as_view(), name='student-record-list-create'),
    path('records/<uuid:pk>/', StudentRecordDetailView.as_view(), name='student-record-detail'),
    path('records/<uuid:pk>/status/', StudentRecordApproveView.as_view(), name='student-record-status'),
    path('certificates/', ManualCertificateListView.as_view(), name='manual-certificate-list'),
    path('certificates/generate/', GenerateManualCertificateView.as_view(), name='manual-certificate-generate'),
    path('stats/', ManagementStatsView.as_view(), name='management-stats'),
]
